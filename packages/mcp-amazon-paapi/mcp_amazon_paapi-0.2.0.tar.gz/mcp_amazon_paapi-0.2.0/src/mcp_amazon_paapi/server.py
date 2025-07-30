import os
import logging
import sys

from mcp.server.fastmcp import FastMCP
from typing import Optional, List
from mcp_amazon_paapi.service import AmazonPAAPIService, SearchItem, SearchSort


logger = logging.getLogger(__name__)


# Create service instance
amazon_service = AmazonPAAPIService()

# Create the MCP server
mcp = FastMCP("Amazon PA-API MCP")


@mcp.tool()
def search_items(search_term: str, category: Optional[str] = None, item_count: Optional[int] = 10, sort_by: Optional[SearchSort] = None) -> List[SearchItem]:
    """
    Search the chosen Amazon marketplace for products —such as books, movies, music, and more — by providing a keyword or a phrase, 
    the product category, and the maximum number of results to return. Sort the results by relevance, price, or customer reviews.
    
    The function calls Amazon's Product Advertising API for Amazon Associates, and every returned item contains a product URL that 
    already includes your Associate partner tag.
    
    Args:
        search_term (str): The search term to use. Examples:
            - "iphone"
            - "harry potter"
            - "sleep mask"
            - "sun glasses"
        category (Optional[str]): The category to search in. Possible values are:
            - All (default)
            - AmazonVideo
            - Apparel
            - Appliances
            - Automotive
            - Baby
            - Beauty
            - Books
            - Classical
            - Computers
            - DigitalMusic
            - Electronics
            - EverythingElse
            - Fashion
            - ForeignBooks
            - GardenAndOutdoor
            - GiftCards
            - GroceryAndGourmetFood
            - Handmade
            - HealthPersonalCare
            - HomeAndKitchen
            - Industrial
            - Jewelry
            - KindleStore
            - Lighting
            - Luggage
            - LuxuryBeauty
            - Magazines
            - MobileApps
            - MoviesAndTV
            - Music
            - MusicalInstruments
            - OfficeProducts
            - PetSupplies
            - Photo
            - Shoes
            - Software
            - SportsAndOutdoors
            - ToolsAndHomeImprovement
            - ToysAndGames
            - VHS
            - VideoGames
            - Watches        
        item_count (Optional[int]): The number of items to return. Defaults to 10.
        sort_by (Optional[SearchSort]): The sort order of the search results. Defaults to None.
    Returns:
        List[SearchItem]: A list of items that match the search criteria.
    """
    return amazon_service.search_items(search_term, category, item_count, sort_by)

def main():
    logging.error(f"Starting Amazon PA-API MCP server for partner tag {os.getenv('PAAPI_PARTNER_TAG')}...")
    mcp.run()

if __name__ == "__main__":
    sys.exit(main())

