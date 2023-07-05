from odmantic import Model


class Games(Model):
    tier: str
    division:str
    leagueId: str
    summonerId: str
    summonerName: str
    
    class Config:
        collection = "DIAMOND I"
