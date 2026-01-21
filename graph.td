graph TD
    %% Entry Point
    Main[main.py] --> Bot[FishingBot]
    Main --> HK[Hotkeys]

    subgraph Core_Engine [Core Engine]
        Bot --> SM[StateMachine]
        Bot --> Det[Detector]
        Bot --> Ctrl[GameController]
        Bot --> Tracker[StatsTracker]
    end

    subgraph Logic_Flow [Logic & States]
        SM --> S_Current{Current State}
        S_Current --> S_Start[StartingState]
        S_Current --> S_Check[CheckingRodState]
        S_Current --> S_Cast[CastingBaitState]
        S_Current --> S_Wait[WaitingForBiteState]
        S_Current --> S_Play[PlayingMinigameState]
        S_Current --> S_Finish[FinishingState]
        
        %% State Interactions
        S_Current -- 1. Analyze Screen --> Det
        S_Current -- 2. Perform Action --> Ctrl
        S_Current -- 3. Transition --> SM
    end

    subgraph Vision_System [Vision & Input]
        Det --> MSS[MSS - Screen Capture]
        Det --> CV2[OpenCV - Template Matching]
        Ctrl --> PAG[PyAutoGUI - Keyboard/Mouse]
    end

    subgraph Configuration [Configuration]
        Bot --> Cfg[Config]
        Cfg --> ScreenCfg[ScreenConfig]
        Cfg --> DetCfg[DetectionConfig]
    end

    %% External Control
    HK -- Toggle Pause/Stop --> Bot