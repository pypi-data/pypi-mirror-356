import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_amazon_paapi.service import AmazonPAAPIService, Item, PAAPIClientConfig, PAAPIClientProtocol, ItemImage
from mcp_amazon_paapi._vendor.paapi5_python_sdk.models import SearchItemsResponse, PartnerType


class TestAmazonPAAPIService:
    """Tests for AmazonPAAPIService"""

    def test_service_init_with_client(self):
        """Test service initialization with provided client"""
        mock_client = Mock(spec=PAAPIClientProtocol)
        service = AmazonPAAPIService(client=mock_client)
        
        assert service._client is mock_client

    def test_service_init_with_config(self):
        """Test service initialization with provided config"""
        config = PAAPIClientConfig(
            access_key="test-key",
            secret_key="test-secret", 
            host="test-host",
            region="test-region",
            marketplace="test-marketplace",
            partner_tag="test-tag"
        )
        service = AmazonPAAPIService(config=config)
        
        assert service._config is config

    @patch.dict(os.environ, {
        'PAAPI_ACCESS_KEY': 'env-key',
        'PAAPI_SECRET_KEY': 'env-secret',
        'PAAPI_PARTNER_TAG': 'env-tag',
        'PAAPI_HOST': 'env-host',
        'PAAPI_REGION': 'env-region',
        'PAAPI_MARKETPLACE': 'env-marketplace'
    })
    def test_config_from_environment(self):
        """Test config creation from environment variables"""
        service = AmazonPAAPIService()
        config = service.config
        
        assert config.access_key == "env-key"
        assert config.secret_key == "env-secret"
        assert config.partner_tag == "env-tag"
        assert config.host == "env-host"
        assert config.region == "env-region"
        assert config.marketplace == "env-marketplace"

    @patch.dict(os.environ, {
        'PAAPI_ACCESS_KEY': 'key',
        'PAAPI_SECRET_KEY': 'secret',
        'PAAPI_PARTNER_TAG': 'tag',
    }, clear=True)
    def test_config_defaults(self):
        """Test config uses defaults when env vars not set"""
        service = AmazonPAAPIService()
        config = service.config
        
        assert config.host == "webservices.amazon.de"
        assert config.region == "eu-west-1"
        assert config.marketplace == "www.amazon.de"
        assert config.partner_type == PartnerType.ASSOCIATES

    def test_search_items_success_with_image(self):
        """Test successful search_items call including image data"""
        # Setup mock response
        mock_item = Mock()
        mock_item.asin = "B123456789"
        mock_item.detail_page_url = "https://amazon.de/test"
        
        # Mock item info with title
        mock_title = Mock()
        mock_title.display_value = "Test Product"
        mock_item_info = Mock()
        mock_item_info.title = mock_title
        mock_item_info.content_rating = None
        mock_item_info.product_info = None
        mock_item.item_info = mock_item_info
        mock_item.offers = None

        # Mock image data
        mock_large_image = Mock()
        mock_large_image.url = "https://example.com/image.jpg"
        mock_large_image.height = 500
        mock_large_image.width = 400

        mock_primary = Mock()
        mock_primary.large = mock_large_image

        mock_images = Mock()
        mock_images.primary = mock_primary
        mock_item.images = mock_images

        # Mock search result
        mock_search_result = Mock()
        mock_search_result.items = [mock_item]
        
        # Mock response
        mock_response = Mock(spec=SearchItemsResponse)
        mock_response.errors = None
        mock_response.search_result = mock_search_result

        # Setup service with mock client
        mock_client = Mock(spec=PAAPIClientProtocol)
        mock_client.search_items.return_value = mock_response
        
        config = PAAPIClientConfig(
            access_key="test", secret_key="test", host="test", 
            region="test", marketplace="test", partner_tag="test"
        )
        service = AmazonPAAPIService(client=mock_client, config=config)

        # Execute
        result = service.search_items("test query")

        # Verify
        assert len(result) == 1
        item = result[0]
        assert item.asin == "B123456789"
        assert item.title == "Test Product"
        assert item.detail_page_url == "https://amazon.de/test"
        assert item.image is not None
        assert item.image.url == "https://example.com/image.jpg"
        assert item.image.height == 500
        assert item.image.width == 400
        mock_client.search_items.assert_called_once()

    def test_search_items_with_category(self):
        """Test search_items with category parameter"""
        mock_response = Mock(spec=SearchItemsResponse)
        mock_response.errors = None
        mock_response.search_result = None

        mock_client = Mock(spec=PAAPIClientProtocol)
        mock_client.search_items.return_value = mock_response
        
        config = PAAPIClientConfig(
            access_key="test", secret_key="test", host="test",
            region="test", marketplace="test", partner_tag="test"
        )
        service = AmazonPAAPIService(client=mock_client, config=config)

        service.search_items("test", category="Books", item_count=5)

        # Verify the request was made with correct parameters
        call_args = mock_client.search_items.call_args[0][0]
        assert call_args.keywords == "test"
        assert call_args.search_index == "Books"
        assert call_args.item_count == 5

    def test_search_items_empty_result(self):
        """Test search_items with empty result"""
        mock_response = Mock(spec=SearchItemsResponse)
        mock_response.errors = None
        mock_response.search_result = None

        mock_client = Mock(spec=PAAPIClientProtocol)
        mock_client.search_items.return_value = mock_response
        
        config = PAAPIClientConfig(
            access_key="test", secret_key="test", host="test",
            region="test", marketplace="test", partner_tag="test"
        )
        service = AmazonPAAPIService(client=mock_client, config=config)

        result = service.search_items("no results")

        assert len(result) == 0
        mock_client.search_items.assert_called_once()

    def test_search_items_with_errors(self):
        """Test search_items when API returns errors"""
        mock_response = Mock(spec=SearchItemsResponse)
        mock_response.errors = ["API Error"]
        mock_response.search_result = None

        mock_client = Mock(spec=PAAPIClientProtocol)
        mock_client.search_items.return_value = mock_response
        
        config = PAAPIClientConfig(
            access_key="test", secret_key="test", host="test",
            region="test", marketplace="test", partner_tag="test"
        )
        service = AmazonPAAPIService(client=mock_client, config=config)

        result = service.search_items("error query")

        assert len(result) == 0
        mock_client.search_items.assert_called_once()

    def test_search_item_dataclass(self):
        """Test Item dataclass creation with image"""
        image = ItemImage(
            url="https://example.com/test.jpg",
            height=800,
            width=600
        )
        
        item = Item(
            asin="B123456789",
            title="Test Title",
            detail_page_url="https://test.com",
            bying_price=19.99,
            audience_rating="PG-13",
            is_adult_product=False,
            image=image
        )
        
        assert item.asin == "B123456789"
        assert item.title == "Test Title"
        assert item.detail_page_url == "https://test.com"
        assert item.bying_price == 19.99
        assert item.audience_rating == "PG-13"
        assert item.is_adult_product is False
        assert item.image == image
        assert item.image.url == "https://example.com/test.jpg"
        assert item.image.height == 800
        assert item.image.width == 600

    def test_search_item_defaults(self):
        """Test Item with default values"""
        item = Item(asin="B123456789")
        
        assert item.asin == "B123456789"
        assert item.title is None
        assert item.detail_page_url is None
        assert item.bying_price is None
        assert item.audience_rating is None
        assert item.is_adult_product is None
        assert item.image is None

    def test_item_image_dataclass(self):
        """Test ItemImage dataclass creation"""
        image = ItemImage(
            url="https://example.com/image.jpg",
            height=1024,
            width=768
        )
        
        assert image.url == "https://example.com/image.jpg"
        assert image.height == 1024
        assert image.width == 768

    def test_get_item_success(self):
        """Test successful get_item call"""
        # Setup mock response
        mock_item = Mock()
        mock_item.asin = "B123456789"
        mock_item.detail_page_url = "https://amazon.de/test"
        
        # Mock item info with title
        mock_title = Mock()
        mock_title.display_value = "Test Product"
        mock_item_info = Mock()
        mock_item_info.title = mock_title
        mock_item_info.content_rating = None
        mock_item_info.product_info = None
        mock_item.item_info = mock_item_info
        mock_item.offers = None

        # Mock image data
        mock_large_image = Mock()
        mock_large_image.url = "https://example.com/image.jpg"
        mock_large_image.height = 500
        mock_large_image.width = 400

        mock_primary = Mock()
        mock_primary.large = mock_large_image

        mock_images = Mock()
        mock_images.primary = mock_primary
        mock_item.images = mock_images

        # Mock items result
        mock_items_result = Mock()
        mock_items_result.items = [mock_item]
        
        # Mock response
        mock_response = Mock()
        mock_response.errors = None
        mock_response.items_result = mock_items_result

        # Setup service with mock client
        mock_client = Mock(spec=PAAPIClientProtocol)
        mock_client.get_items.return_value = mock_response
        
        config = PAAPIClientConfig(
            access_key="test", secret_key="test", host="test", 
            region="test", marketplace="test", partner_tag="test"
        )
        service = AmazonPAAPIService(client=mock_client, config=config)

        # Execute
        result = service.get_item("B123456789")

        # Verify
        assert result is not None
        assert result.asin == "B123456789"
        assert result.title == "Test Product"
        assert result.detail_page_url == "https://amazon.de/test"
        assert result.image is not None
        assert result.image.url == "https://example.com/image.jpg"
        assert result.image.height == 500
        assert result.image.width == 400
        mock_client.get_items.assert_called_once()

    def test_get_item_with_errors(self):
        """Test get_item when API returns errors"""
        mock_response = Mock()
        mock_response.errors = ["API Error"]
        mock_response.items_result = None

        mock_client = Mock(spec=PAAPIClientProtocol)
        mock_client.get_items.return_value = mock_response
        
        config = PAAPIClientConfig(
            access_key="test", secret_key="test", host="test",
            region="test", marketplace="test", partner_tag="test"
        )
        service = AmazonPAAPIService(client=mock_client, config=config)

        result = service.get_item("B123456789")

        assert result is None
        mock_client.get_items.assert_called_once()

    def test_get_item_not_found(self):
        """Test get_item when item is not found"""
        mock_response = Mock()
        mock_response.errors = None
        mock_response.items_result = None

        mock_client = Mock(spec=PAAPIClientProtocol)
        mock_client.get_items.return_value = mock_response
        
        config = PAAPIClientConfig(
            access_key="test", secret_key="test", host="test",
            region="test", marketplace="test", partner_tag="test"
        )
        service = AmazonPAAPIService(client=mock_client, config=config)

        result = service.get_item("B123456789")

        assert result is None
        mock_client.get_items.assert_called_once()

    def test_get_item_empty_result(self):
        """Test get_item when items_result has no items"""
        mock_items_result = Mock()
        mock_items_result.items = []
        
        mock_response = Mock()
        mock_response.errors = None
        mock_response.items_result = mock_items_result

        mock_client = Mock(spec=PAAPIClientProtocol)
        mock_client.get_items.return_value = mock_response
        
        config = PAAPIClientConfig(
            access_key="test", secret_key="test", host="test",
            region="test", marketplace="test", partner_tag="test"
        )
        service = AmazonPAAPIService(client=mock_client, config=config)

        result = service.get_item("B123456789")

        assert result is None
        mock_client.get_items.assert_called_once() 