"""
1WorldSync Content1 API Client

This module provides a client for interacting with the 1WorldSync Content1 API.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from .content1_auth import Content1HMACAuth
from .exceptions import APIError, AuthenticationError
from .criteria import ProductCriteria, DateRangeCriteria, SortField
from .models import Content1ProductResults, Content1HierarchyResults


class Content1Client:
    """
    Client for the 1WorldSync Content1 API
    
    This class provides methods for interacting with the 1WorldSync Content1 API,
    handling authentication, request construction, and response parsing.
    """
    
    def __init__(self, app_id=None, secret_key=None, gln=None, api_url=None, timeout=30):
        """
        Initialize the 1WorldSync Content1 API client
        
        Args:
            app_id (str, optional): The application ID provided by 1WorldSync. 
                                   If None, will try to get from ONEWORLDSYNC_APP_ID environment variable.
            secret_key (str, optional): The secret key provided by 1WorldSync.
                                       If None, will try to get from ONEWORLDSYNC_SECRET_KEY environment variable.
            gln (str, optional): Global Location Number for the user.
                               If None, will try to get from ONEWORLDSYNC_USER_GLN environment variable.
            api_url (str, optional): The API URL to use. 
                                    If None, will try to get from ONEWORLDSYNC_CONTENT1_API_URL environment variable.
                                    Defaults to production API if not specified.
            timeout (int, optional): Request timeout in seconds. Defaults to 30.
        """
        # Get credentials from environment variables if not provided
        self.app_id = app_id or os.environ.get('ONEWORLDSYNC_APP_ID')
        self.secret_key = secret_key or os.environ.get('ONEWORLDSYNC_SECRET_KEY')
        self.gln = gln or os.environ.get('ONEWORLDSYNC_USER_GLN')
        
        # Get API URL from environment variable if not provided
        default_api_url = 'https://content1-api.1worldsync.com'
        self.api_url = api_url or os.environ.get('ONEWORLDSYNC_CONTENT1_API_URL', default_api_url)
        
        # Remove trailing slash if present
        if self.api_url.endswith('/'):
            self.api_url = self.api_url[:-1]
        
        # Validate required parameters
        if not self.app_id or not self.secret_key:
            raise ValueError("ONEWORLDSYNC_APP_ID and ONEWORLDSYNC_SECRET_KEY must be provided either as parameters or environment variables")
        
        self.auth = Content1HMACAuth(self.app_id, self.secret_key, self.gln)
        self.timeout = timeout
    
    def _make_request(self, method, path, query_params=None, data=None):
        """
        Make a request to the 1WorldSync Content1 API
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            path (str): API endpoint path
            query_params (dict, optional): Query parameters. Defaults to None.
            data (dict, optional): Request body data. Defaults to None.
            
        Returns:
            dict: API response parsed as JSON
            
        Raises:
            AuthenticationError: If authentication fails
            APIError: If the API returns an error
        """
        # Initialize parameters if None
        if query_params is None:
            query_params = {}
        
        # Add timestamp to query parameters
        timestamp = self.auth.generate_timestamp()
        query_params['timestamp'] = timestamp
        
        # Build the URI (path + query parameters) - exactly as in TypeScript implementation
        uri = path
        if query_params:
            # Sort query parameters to ensure consistent order
            sorted_params = sorted(query_params.items())
            query_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
            uri = f"{path}?{query_string}"
        
        # Get authentication headers
        headers = self.auth.generate_auth_headers(uri)
        
        # Build the full URL
        url = f"{self.api_url}{uri}"
        # Debug Print - equivalent curl command for debugging
        # data_str = "" if data is None else f" -d '{json.dumps(data)}'"
        # headers_str = " ".join([f"-H \"{k}: {v}\"" for k, v in headers.items()])
        # curl_cmd = f"curl -X {method} \"{url}\" {headers_str}{data_str}"
        # print(f"Equivalent curl command:\n{curl_cmd}")
        
        try:
            # Make the request
            response = requests.request(
                method,
                url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            
            # Check for errors
            if response.status_code == 401:
                error_message = f"Authentication failed: {response.text}"
                print(f"Authentication error details: Status {response.status_code}, Response: {response.text}")
                print(f"Request URL: {url}")
                print(f"Request headers: {headers}")
                raise AuthenticationError(error_message)
            
            if response.status_code >= 400:
                print(f"API error details: Status {response.status_code}, Response: {response.text}")
                raise APIError(
                    response.status_code,
                    response.text,
                    response
                )
            
            # Return empty dict for 204 No Content
            if response.status_code == 204:
                return {}
            
            # Parse response
            return response.json()
        
        except requests.exceptions.RequestException as e:
            raise APIError(0, str(e))
    
    def count_products(self, criteria=None):
        """
        Count products using the Content1 API
        
        Args:
            criteria (dict or ProductCriteria, optional): Search criteria. Defaults to empty dict.
            
        Returns:
            int: Count of products matching the criteria
        """
        if criteria is None:
            criteria = {}
        elif isinstance(criteria, ProductCriteria):
            criteria = criteria.build()
        
        response = self._make_request('POST', '/V1/product/count', data=criteria)
        return response.get('count', 0)
    
    def fetch_products(self, criteria=None, page_size=1000):
        """
        Fetch products using the Content1 API
        
        Args:
            criteria (dict or ProductCriteria, optional): Search criteria. Defaults to empty dict.
            page_size (int, optional): Number of products to return per page. Defaults to 1000.
            
        Returns:
            Content1ProductResults: Product fetch results
        """
        if criteria is None:
            criteria = {}
        elif isinstance(criteria, ProductCriteria):
            criteria = criteria.build()
        
        query_params = {'pageSize': page_size}
        response = self._make_request('POST', '/V1/product/fetch', query_params=query_params, data=criteria)
        return Content1ProductResults(response)
    
    def fetch_hierarchies(self, criteria=None, page_size=1000):
        """
        Fetch product hierarchies using the Content1 API
        
        Args:
            criteria (dict or ProductCriteria, optional): Search criteria. Defaults to empty dict.
            page_size (int, optional): Number of hierarchies to return per page. Defaults to 1000.
            
        Returns:
            Content1HierarchyResults: Hierarchy fetch results
        """
        if criteria is None:
            criteria = {}
        elif isinstance(criteria, ProductCriteria):
            criteria = criteria.build()
        
        query_params = {'pageSize': page_size}
        response = self._make_request('POST', '/V1/product/hierarchy', query_params=query_params, data=criteria)
        return Content1HierarchyResults(response)
    
    def fetch_products_by_gtin(self, gtins, page_size=1000):
        """
        Fetch products by GTIN
        
        Args:
            gtins (list): List of GTINs to fetch
            page_size (int, optional): Number of products to return per page. Defaults to 1000.
            
        Returns:
            dict: Product fetch results
        """
        criteria = {
            'gtin': gtins
        }
        return self.fetch_products(criteria, page_size)
    
    def fetch_products_by_ip_gln(self, ip_gln, page_size=1000):
        """
        Fetch products by Information Provider GLN
        
        Args:
            ip_gln (str): Information Provider GLN
            page_size (int, optional): Number of products to return per page. Defaults to 1000.
            
        Returns:
            dict: Product fetch results
        """
        criteria = {
            'ipGln': ip_gln
        }
        return self.fetch_products(criteria, page_size)
    
    def fetch_products_by_target_market(self, target_market, page_size=1000):
        """
        Fetch products by target market
        
        Args:
            target_market (str): Target market code (e.g., 'US')
            page_size (int, optional): Number of products to return per page. Defaults to 1000.
            
        Returns:
            dict: Product fetch results
        """
        criteria = {
            'targetMarket': target_market
        }
        return self.fetch_products(criteria, page_size)
    
    def fetch_next_page(self, previous_response, page_size=1000, original_criteria=None):
        """
        Fetch the next page of products using the searchAfter value from a previous response
        
        Args:
            previous_response (dict or Content1ProductResults): Previous response from fetch_products
            page_size (int, optional): Number of products to return per page. Defaults to 1000.
            original_criteria (dict or ProductCriteria, optional): Original search criteria to preserve. Defaults to None.
            
        Returns:
            Content1ProductResults: Next page of product fetch results
        """
        # Handle Content1ProductResults object
        if isinstance(previous_response, Content1ProductResults):
            search_after = previous_response.search_after
        else:
            if 'searchAfter' not in previous_response:
                raise ValueError("Previous response does not contain searchAfter value")
            search_after = previous_response['searchAfter']
        
        # Handle original criteria
        if original_criteria is None:
            criteria = {}
        elif isinstance(original_criteria, ProductCriteria):
            criteria = original_criteria.build()
        else:
            criteria = original_criteria.copy()
        
        # Add searchAfter parameter
        criteria['searchAfter'] = search_after
        
        return self.fetch_products(criteria, page_size)
    def fetch_products_by_date_range(self, from_date, to_date, target_market=None, page_size=1000):
        """
        Fetch products by last modified date range
        
        Args:
            from_date (str): Start date in YYYY-MM-DD format
            to_date (str): End date in YYYY-MM-DD format
            target_market (str, optional): Target market code (e.g., 'US'). Defaults to None.
            page_size (int, optional): Number of products to return per page. Defaults to 1000.
            
        Returns:
            Content1ProductResults: Product fetch results
        """
        criteria = ProductCriteria()
        criteria.with_last_modified_date(DateRangeCriteria.between(from_date, to_date))
        
        if target_market:
            criteria.with_target_market(target_market)
        
        return self.fetch_products(criteria, page_size)
    
    def fetch_products_last_30_days(self, target_market=None, page_size=1000):
        """
        Fetch products modified in the last 30 days
        
        Args:
            target_market (str, optional): Target market code (e.g., 'US'). Defaults to None.
            page_size (int, optional): Number of products to return per page. Defaults to 1000.
            
        Returns:
            Content1ProductResults: Product fetch results
        """
        criteria = ProductCriteria()
        criteria.with_last_modified_date(DateRangeCriteria.last_30_days())
        
        if target_market:
            criteria.with_target_market(target_market)
        
        return self.fetch_products(criteria, page_size)
    
    def fetch_products_by_brand(self, brand_name, target_market=None, page_size=1000):
        """
        Fetch products by brand name
        
        Args:
            brand_name (str): Brand name to search for
            target_market (str, optional): Target market code (e.g., 'US'). Defaults to None.
            page_size (int, optional): Number of products to return per page. Defaults to 1000.
            
        Returns:
            Content1ProductResults: Product fetch results
        """
        criteria = ProductCriteria().with_brand_name(brand_name)
        
        if target_market:
            criteria.with_target_market(target_market)
        
        return self.fetch_products(criteria, page_size)
    
    def fetch_products_by_gpc_code(self, gpc_code, target_market=None, page_size=1000):
        """
        Fetch products by GPC code
        
        Args:
            gpc_code (str): GPC code to search for
            target_market (str, optional): Target market code (e.g., 'US'). Defaults to None.
            page_size (int, optional): Number of products to return per page. Defaults to 1000.
            
        Returns:
            Content1ProductResults: Product fetch results
        """
        criteria = ProductCriteria().with_gpc_code(gpc_code)
        
        if target_market:
            criteria.with_target_market(target_market)
        
        return self.fetch_products(criteria, page_size)
    
    def fetch_products_by_upc(self, upc_code, target_market=None, page_size=1000):
        """
        Fetch products by UPC code
        
        Args:
            upc_code (str): UPC code to search for
            target_market (str, optional): Target market code (e.g., 'US'). Defaults to None.
            page_size (int, optional): Number of products to return per page. Defaults to 1000.
            
        Returns:
            Content1ProductResults: Product fetch results
        """
        criteria = ProductCriteria().with_upc_code(upc_code)
        
        if target_market:
            criteria.with_target_market(target_market)
        
        return self.fetch_products(criteria, page_size)