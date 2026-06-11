# Configuration parameters for the consumer choice ABM

class Config:
    # Model parameters (matching NetLogo interface)
    NUM_CONSUMERS = 100
    AVG_CONNECTIONS = 5
    INIT_ORANGE_PCT = 50  # percentage
    QUALITY_ORANGE = 0.45
    QUALITY_BLUE = 0.50
    NORM_INFLUENCE = 0.1
    INFO_EXCHANGE = 0.50
    EXPLORATION = 0.01
    
    # Simulation settings
    SEED = 42
    NUM_STEPS = 100
    WORLD_SIZE = 800  # for random positions
    
    @classmethod
    def get_quality_list(cls):
        return [cls.QUALITY_ORANGE, cls.QUALITY_BLUE]