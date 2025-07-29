"""anuvaad-rev translator module for Indian language translations"""

import json
import time
import random
import requests
from typing import Dict, Optional, List, Tuple
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from langdetect import detect, detect_langs, LangDetectException
from .constants import SUPPORTED_LANGUAGES, API_ENDPOINT, SERVICE_ID
from .user_agents import get_random_user_agent

class IndicTranslator:
    """Class for handling translations using AI4Bharat's IndicTrans2 API with rate limit bypass"""
    
    def __init__(self, max_retries: int = 3, session_refresh_interval: int = 3600):
        """
        Initialize translator with session management
        
        Args:
            max_retries: Maximum number of retries for failed requests
            session_refresh_interval: Interval in seconds to refresh session
        """
        self.session_refresh_interval = session_refresh_interval
        self.last_session_refresh = 0
        self.session = self._create_session(max_retries)
        self.last_request_time = 0
        self.min_request_interval = 2  # Minimum seconds between requests
        self.max_request_interval = 5  # Maximum seconds between requests
        
    def _create_session(self, max_retries: int) -> requests.Session:
        """Create a new session with retry strategy"""
        session = requests.Session()
        
        # Configure retry strategy with exponential backoff
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=2,  # Exponential backoff
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        
        # Mount adapter with retry strategy
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _refresh_session_if_needed(self):
        """Refresh session if interval has elapsed"""
        current_time = time.time()
        if current_time - self.last_session_refresh >= self.session_refresh_interval:
            self.session = self._create_session(max_retries=3)
            self.last_session_refresh = current_time
            
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with random user agent"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": get_random_user_agent(),
            "Origin": "https://ai4bharat.iitm.ac.in",
            "Referer": "https://ai4bharat.iitm.ac.in/",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
    
    def _wait_between_requests(self):
        """Implement dynamic wait time between requests"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        # Random wait time between min and max interval
        wait_time = random.uniform(self.min_request_interval, self.max_request_interval)
        
        if elapsed < wait_time:
            time.sleep(wait_time - elapsed)
            
        self.last_request_time = time.time()

    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text
        
        Args:
            text: Text to detect language for
            
        Returns:
            Detected language code or 'en' if detection fails
            
        Note:
            Returns 'en' for non-supported languages since English is the default source
        """
        try:
            detected = detect(text)
            # Map some common language codes
            lang_mapping = {
                'hi': 'hi',
                'ta': 'ta',
                'te': 'te',
                'ml': 'ml',
                'kn': 'kn',
                'bn': 'bn',
                'gu': 'gu',
                'mr': 'mr',
                'pa': 'pa',
                'ur': 'ur'
            }
            return lang_mapping.get(detected, 'en')
        except LangDetectException:
            return 'en'

    def detect_language_confidence(self, text: str) -> List[Tuple[str, float]]:
        """
        Detect language with confidence scores
        
        Args:
            text: Text to detect language for
            
        Returns:
            List of tuples containing (language_code, confidence_score)
        """
        try:
            detected_langs = detect_langs(text)
            return [(lang.lang, lang.prob) for lang in detected_langs]
        except LangDetectException:
            return [('en', 1.0)]

    def get_language_name(self, lang_code: str) -> Optional[str]:
        """
        Get language name from language code
        
        Args:
            lang_code: Language code
            
        Returns:
            Language name if code is supported, None otherwise
        """
        return SUPPORTED_LANGUAGES.get(lang_code)

    def get_language_code(self, language_name: str) -> Optional[str]:
        """
        Get language code from language name
        
        Args:
            language_name: Name of the language
            
        Returns:
            Language code if name is supported, None otherwise
        """
        for code, name in SUPPORTED_LANGUAGES.items():
            if name.lower() == language_name.lower():
                return code
        return None

    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported language codes and names"""
        return SUPPORTED_LANGUAGES.copy()

    def get_supported_language_codes(self) -> List[str]:
        """Get list of supported language codes"""
        return list(SUPPORTED_LANGUAGES.keys())

    def get_supported_language_names(self) -> List[str]:
        """Get list of supported language names"""
        return list(SUPPORTED_LANGUAGES.values())
        
    def translate(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> Optional[str]:
        """
        Translate text using IndicTrans2
        
        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code (if None, will be auto-detected)
            
        Returns:
            Translated text if successful, None otherwise
            
        Raises:
            ValueError: If language codes are invalid
            RequestException: If API request fails
        """
        # Auto-detect source language if not provided
        if source_lang is None:
            source_lang = self.detect_language(text)
            
        # Validate languages
        if source_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Source language '{source_lang}' not supported")
        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Target language '{target_lang}' not supported")
            
        # Rate limit handling
        self._wait_between_requests()
            
        # Refresh session if needed
        self._refresh_session_if_needed()
            
        # Prepare request payload
        payload = {
            "input": text,
            "task": "translation",
            "track": True,
            "serviceId": SERVICE_ID,
            "sourceLanguage": source_lang,
            "targetLanguage": target_lang
        }
        
        try:
            # Make API request with current session and random user agent
            response = self.session.post(
                API_ENDPOINT,
                headers=self._get_headers(),
                json=payload,
                timeout=30  # 30 seconds timeout
            )
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            if "output" in result and len(result["output"]) > 0:
                return result["output"][0]["target"]
            return None
            
        except requests.exceptions.RequestException as e:
            # Increase wait time on failure
            self.min_request_interval = min(self.min_request_interval * 1.5, 10)
            self.max_request_interval = min(self.max_request_interval * 1.5, 15)
            raise Exception(f"Translation request failed: {str(e)}")