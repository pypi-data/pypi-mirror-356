import json
from pydantic import Field
from ..utils.fastf1_utils import get_laps, get_specific_lap, get_session
import fastf1.plotting as f1_plotting

def register_fastf1_tools(mcp):
    """Register all F1 analysis tools with the MCP server"""

    @mcp.tool(name="get_fastest_lap")
    async def get_fastest_lap(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'."),
        driver: str = Field(description="The driver's name. If you don't have a specific driver in mind, you can leave this blank to get the fastest lap for all drivers"),
    ) -> json:
        """Get the fastest laps for a driver in a session. In case no driver is specified, it will return the fastest laps for all drivers"""

        laps = get_laps(type_session, year, round, session, driver)
        lap = get_specific_lap(
                laps,
                get_general_fastest_lap = False if driver else True,
                get_personal_fastest_lap= True if driver else False
            )
        return lap.to_json()

    @mcp.tool(name="get_lap")
    async def get_lap(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'."),
        driver: str = Field(description="The driver's names."),
        lap_number: int = Field(description="The lap number"),
    ) -> json:
        """Get specific lap from a driver in a session"""

        laps = get_laps(type_session, year, round, session, driver)
        lap = get_specific_lap(laps, lap_number)
        return lap.to_json()

    @mcp.tool(name="get_top_speed")
    async def get_top_speed(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'."),
        driver: str = Field(description="The driver's name. If you don't have a specific driver in mind, you can leave this blank to get the fastest lap for all drivers"),
    ) -> int:
        """Get the top speed for a driver in a session. In case no driver is specified, it will return the highest top speed for all drivers"""

        laps = get_laps(type_session, year, round, session, driver)
        max_speed = max(laps["SpeedI1"], laps["SpeedI2"], laps["SpeedFL"], laps["SpeedST"])
        return max_speed

    @mcp.tool(name="get_total_laps")
    async def get_total_laps(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'."),
        driver: str = Field(description="The driver's name. If you don't have a specific driver in mind, you can leave this blank to get the fastest lap for all drivers"),
    ) -> int:
        """Get the total laps for a driver in a session. In case no driver is specified, it will return the total laps for all drivers"""

        laps = get_laps(type_session, year, round, session, driver)
        return len(laps)

    @mcp.tool(name="get_driver_team")
    async def get_driver_team(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'."),
        driver: str = Field(description="The driver's name."),
    ) -> str:
        """Get the driver’s team name."""

        session = get_session(type_session, year, round, session)
        return f1_plotting.get_team_name_by_driver(identifier=driver, session=session)

    @mcp.tool(name="get_team_driver")
    async def get_team_driver(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event, such as 'FP1', 'FP2', 'Q', 'R', or 'Sprint'."),
        team: str = Field(description="The team's name."),
    ) -> str:
        """Get the team's driver name."""

        session = get_session(type_session, year, round, session)
        return f1_plotting.get_driver_names_by_team(identifier=team, session=session)

    @mcp.tool(name="get_box_laps")
    async def get_box_laps(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event 'R'"),
        driver: str = Field(description="The driver's name."),
    ) -> json:
        """Get laps where the driver was in the pit box."""

        laps = get_laps(type_session, year, round, session,driver)
        box_laps = laps.pick_box_laps(which="both")[["Time","Driver","LapNumber","Compound","PitOutTime","PitInTime"]]
        return box_laps.to_json()

    @mcp.tool(name="get_deleted_laps")
    async def get_deleted_laps(
        type_session: str = Field(description="Type of session in general terms: official or pretest (pre-session test)"),
        year: int = Field(description="The year of the season when the session was held"),
        round: int = Field(description="The round number of the championship, for example 1 for the first Grand Prix."),
        session: str = Field(description="The exact name of the session within the event 'R'"),
        driver: str = Field(description="The driver's name."),
    ) -> json:
        """Get laps where the driver was in the pit box."""

        laps = get_laps(type_session, year, round, session, driver)
        deleted_laps = laps[laps["Deleted"] == True][["Time","Driver","LapNumber","Deleted","DeletedReason"]]
        return deleted_laps.to_json()

