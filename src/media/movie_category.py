from enum import Enum, auto

class MovieCategory(Enum):
    
    NEW = auto()
    RANDOM = auto()
    GENERAL = auto()
    
    
    def get_attributes(self):
        
        if self == MovieCategory.NEW:
            return ['title', 'year', 'plot', 'onlineRating', 'url', 'fetched']
        
        if self == MovieCategory.RANDOM:
            return ['title', 'year', 'plot', 'onlineRating', 'url', 'watched']
        
        if self == MovieCategory.GENERAL:
            return ['title', 'year', 'plot', 'onlineRating', 'url', 'fetched']