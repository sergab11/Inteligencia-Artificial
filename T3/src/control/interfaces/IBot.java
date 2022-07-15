package control.interfaces;

import INF1771_GameClient.Dto.PlayerInfo;
import control.drone.LookOut;

public interface IBot {
    int getX();
    int getY();
    int getEnergy();
    int getTick();
    PlayerInfo.Direction getDir();
    LookOut getUltimaObservacao();
}
