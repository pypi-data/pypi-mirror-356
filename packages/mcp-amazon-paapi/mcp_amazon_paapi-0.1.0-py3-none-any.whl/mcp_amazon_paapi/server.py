import os
import logging
import sys

from mcp.server.fastmcp import FastMCP
from typing import Optional, List
from mcp_amazon_paapi.service import AmazonPAAPIService, SearchItem


logger = logging.getLogger(__name__)


# Create service instance
amazon_service = AmazonPAAPIService()

# Create the MCP server
mcp = FastMCP("Amazon PA-API MCP")


@mcp.tool()
def search_items(search_term: str, category: Optional[str] = None, item_count: Optional[int] = 10) -> List[SearchItem]:
    """
    Search for items (products, books, movies, music, etc.) on the given Amazon marketplace with the given search term (a list of keywords), 
    the category to search in and the number of items to return.
    Args:
        search_term: The search term to use. Examples:
            - "iphone"
            - "harry potter"
            - "sleep mask"
            - "sun glasses"
        category: The category to search in. Possible values are:
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
        item_count: The number of items to return.
    Returns:
        A list of items that match the search criteria.
    """
    return amazon_service.search_items(search_term, category, item_count)

def main():
    logging.error(f"Starting Amazon PA-API MCP server for partner tag {os.getenv('PAAPI_PARTNER_TAG')}...")
    mcp.run()

if __name__ == "__main__":
    sys.exit(main())