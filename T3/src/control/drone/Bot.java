package control.drone;

import INF1771_GameClient.Dto.PlayerInfo;
import INF1771_GameClient.Dto.ScoreBoard;
import INF1771_GameClient.Dto.ShotInfo;
import INF1771_GameClient.Socket.HandleClient;
import control.Base;
import control.enums.Action;
import control.interfaces.IBot;
import control.map.Field;
import control.server.ConnectionListener;
import control.server.GameListener;
import control.server.Log;
import draw.View;
import control.server.HandlerServer;

import javax.swing.*;
import java.util.*;

public class Bot implements Runnable, IBot {

    public static long tickAtual;
    public static long ping = 0;

    public HandleClient client;                             // client para conexao
    public Map<Long, PlayerInfo> listaJogadores;            // lista dos jogadores
    public List<ShotInfo> listaDisparos;                    // lista de disparos
    public List<ScoreBoard> listaScores;                    // lista de scores
    public Log log;                                         // log do jogo
    public HandlerServer handlerServer;                                   // envio de mensagens
    public long time;                                       // tempo decorrido
    public LookOut ultimaObservacao;         			// observacao do bot

    public Brain brain;

    public int x;
    public int y;
    public int tick;
    public PlayerInfo.Direction dir;
    public PlayerInfo.State state;
    public long score;
    public int energy;
    public int thinkingTime;

    public String ultimoAcerto;
    public int ultimoTickAcerto;

    public JFrame tela;

    private void config() {
        this.client = new HandleClient();
        Field.iniciar();
        this.log = new Log();
        this.handlerServer = new HandlerServer(this.client);

        this.brain = new Brain(this);

        this.listaJogadores = new HashMap<>();
        this.listaDisparos = new ArrayList<>();
        this.listaScores = new ArrayList<>();
        this.ultimaObservacao = new LookOut();

        this.time = 0;

        // cria um listener de conexao, e adiciona no client
        this.client.addChangeStatusListener(new ConnectionListener(this.client));

        // cria um listener de commando, passando o bot para atualizar minhas variaveis
        this.client.addCommandListener(new GameListener(this));

        // inicia a conexao
        this.client.connect(Base.url);

        tela = new View(this);

        Thread thread = new Thread(this);
        thread.start();
    }

    /* Cria um novo bot, rodando as configuracoes padrao */
    public Bot() {
        config();
    }

    public void dormir(int ms) {
        Field.fazerTick(ms);
        if (ms < 0) { return; }
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void limparObservacoes() {
        this.ultimaObservacao.reset();
    }

    public void exibirScore() {
        try {
            System.out.println("==== BOARD ====");
            System.out.printf("Tempo: %d\n", time);
            System.out.printf("Status: %s\n", state.toString());
            for (ScoreBoard sb : this.listaScores) {
                String s = String.format("%s (%s): score=%d, energy=%d",
                        sb.name,
                        sb.connected ? "connected" : "not connected",
                        sb.score,
                        sb.energy);
                System.out.println(s);
            }
        }
        catch (Exception ignored) {}
    }

    /* IMPLEMENTACOES DE IBOT */
    public int getX() { return this.x; }
    public int getY() { return this.y; }
    public int getEnergy() { return this.energy; }
    public int getTick() { return this.tick; }
    public PlayerInfo.Direction getDir() { return this.dir; }
    public LookOut getUltimaObservacao() { return this.ultimaObservacao; }
    public void antiCheat(String acertoAtual) {
        int tempo = (int) System.currentTimeMillis() - ultimoTickAcerto;
        if (acertoAtual.equals(this.ultimoAcerto) && tempo < Base.timerMinimo ) {
            this.handlerServer.enviarMensagem(String.format(
                    "Cheating? %s me acertou em %d ms de diferenca (permitido: %d ms)",
                    ultimoAcerto, tempo, Base.timerMinimo));
        }
    }

    /* Roda o bot */
    @Override
    public void run() {
        int timer = 0;
        long tempoExec;
        boolean emPartida = false;
        Action acao = Action.NADA;


        while (true) {
            if (state == PlayerInfo.State.game) {

                // dorme
                if (acao == Action.ATIRAR) dormir(Base.timerMinimo - this.thinkingTime);
                else dormir(Base.timerNormal - this.thinkingTime);

                // caso seja o inicio da partida
                if (!emPartida) {
                    this.tick = 0;
                    emPartida = true;
                    this.handlerServer.pedirStatus();
                    this.handlerServer.pedirObservacao();
                    dormir(Base.timerNormal);
                }

                // atualiza as variaveis de contagem
                this.tick += 1;
                tempoExec = System.currentTimeMillis();

                // faz a acao
                acao = this.brain.pensar();
                this.handlerServer.enviarAction(acao);

                // pede as proximas coisas
                limparObservacoes();
                this.handlerServer.pedirObservacao();
                this.handlerServer.pedirStatus();
                this.handlerServer.pedirStatusGame();
                Bot.tickAtual = System.currentTimeMillis();

                // atualiza as coisas
                this.tela.repaint();
                this.thinkingTime = (int) (System.currentTimeMillis() - tempoExec);
            } else {
                dormir(Base.timerLento);
                if (emPartida) {
                    this.handlerServer.enviarMensagem("gg");
                }

                emPartida = false;
                Field.iniciar();
                if (timer == 5) {
                    this.handlerServer.pedirScoreboard();
                    exibirScore();
                    timer = 0;
                }
                timer += 1;

                this.handlerServer.pedirStatusGame();
            }
            this.log.printLast();
        }
    }
}
