package control.server;

import INF1771_GameClient.Socket.*;
import control.Base;

public class ConnectionListener implements CommandListener{
    HandleClient client;
    public ConnectionListener(HandleClient client) {
        this.client = client;
    }

    public void receiveCommand(String[] cmd) {
        if (this.client.connected) {
            System.out.println("Conectado!");
            this.client.sendName(Base.nomeJogador);       // envia meu nome
            this.client.sendColor(Base.corDefault);       // envia minha cor
            this.client.sendRequestGameStatus();            // pega o status
            this.client.sendRequestUserStatus();            // me atualiza
            this.client.sendRequestObservation();           // da uma observacao
        }
        else {
            System.out.println("Desconectado! Caiu...");
        }
    }
}
