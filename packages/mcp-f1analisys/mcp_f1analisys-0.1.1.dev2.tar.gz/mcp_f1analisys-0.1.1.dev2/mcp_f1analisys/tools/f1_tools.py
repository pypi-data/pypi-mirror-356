from pydantic import Field
from mcp.server.fastmcp import Image
from ..utils.http_client import F1AnalysisClient
from ..utils.path_utils import get_full_path

# Global client instance
client = F1AnalysisClient()

async def get_image_analysis(params: list) -> Image:
    """Get F1 analysis image from API"""
    full_path = get_full_path(params)
    image_data = await client.get_image(full_path)
    return Image(data=image_data, format="png")

def register_f1_tools(mcp):
    """Register all F1 analysis tools with the MCP server"""
    
    @mcp.tool(name="top_speed")
    async def get_top_speed(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'.")
        ) -> Image:
        """Get F1 top speed data visualization from the session"""
        return await get_image_analysis([type_session, "top_speed", year, round, session])

    @mcp.tool(name="braking")
    async def get_braking(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'.")
        ) -> Image:
        """Get F1 average braking data visualization from the session"""
        return await get_image_analysis([type_session, "braking", year, round, session])

    @mcp.tool(name="throttle")
    async def get_throttle(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'.")
        ) -> Image:
        """Get F1 average throttle data visualization from the session"""
        return await get_image_analysis([type_session, "throttle", year, round, session])

    @mcp.tool(name="fastest_laps")
    async def get_fastest_laps(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'.")
        ) -> Image:
        """Get F1 fastest laps data visualization from the session"""
        return await get_image_analysis([type_session, "fastest_laps", year, round, session])

    @mcp.tool(name="lap_time_average")
    async def get_lap_time_average(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'.")
        ) -> Image:
        """Get F1 lap time average data visualization from the session"""
        return await get_image_analysis([type_session, "lap_time_average", year, round, session])

    @mcp.tool(name="team_performace")
    async def get_team_performace(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'.")
        ) -> Image:
        """Get F1 team performance data visualization from the session"""
        return await get_image_analysis([type_session, "team_performace", year, round, session])

    @mcp.tool(name="race_position_evolution")
    async def get_race_position_evolution(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'. In this case, this image can only take 'R' and 'Q' as session.")
        ) -> Image:
        """Get F1 race position evolution data visualization from the session"""
        return await get_image_analysis([type_session, "race_position_evolution", year, round, session])

    @mcp.tool(name="lap_time_distribution")
    async def get_lap_time_distribution(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test). In this only this image can only take 'official' as type_session"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'. In this case, this image can only take 'R' and 'Q' as session.")
        ) -> Image:
        """Get F1 lap time distribution data visualization from the session"""
        return await get_image_analysis([type_session, "lap_time_distribution", year, round, session])

    @mcp.tool(name="fastest_drivers_compound")
    async def get_fastest_drivers_compound(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'.")
        ) -> Image:
        """Get F1 fatest drivers compound data visualization from the session"""
        return await get_image_analysis([type_session, "fastest_drivers_compound", year, round, session])

    @mcp.tool(name="long_runs")
    async def get_long_runs(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'."),
        drivers_laps_range: dict = Field(
            description="""Dictionary list where the key is the name of the driver and value is driver range laps selected
                        E.G:{ 
                                LEC: [8,15],
                                VER: [9,12],
                                PIA: [10,14]
                            }"""
        ),
        ) -> Image:
        """Get a long run analysis of specific drivers between selected laps of the session"""
        return await get_image_analysis([type_session, "long_runs", year, round, session, drivers_laps_range])

    @mcp.tool(name="track_dominance")
    async def get_track_dominance(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'."),
        drivers_laps_range: dict = Field(
            description="""Dictionary list where the key is the name of the driver and value is the lap selected
                        E.G:{ 
                                LEC: [8],
                                VER: [9],
                                PIA: [10]
                            }"""
            )
        ) -> Image:
        """Get F1 track dominance data visualization from the session"""
        return await get_image_analysis([type_session, "track_dominance", year, round, session, drivers_laps_range])

    @mcp.tool(name="comparative_lap_time")
    async def get_comparative_lap_time(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'."),
        drivers_laps_range: dict = Field(
            description="""Dictionary list where the key is the name of the driver and value is the lap selected
                        E.G:{ 
                                LEC: [8],
                                VER: [9],
                                PIA: [10]
                            }"""
            )
        ) -> Image:
        """Get F1 comparative lap time data visualization from the session"""
        return await get_image_analysis([type_session, "comparative_lap_time", year, round, session, drivers_laps_range])