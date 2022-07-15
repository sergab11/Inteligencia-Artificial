package control.server;

import INF1771_GameClient.Dto.PlayerInfo;
import INF1771_GameClient.Dto.ScoreBoard;
import INF1771_GameClient.Socket.*;
import control.drone.Bot;
import control.Base;

import java.awt.*;
import java.util.ArrayList;

public class GameListener implements CommandListener {

    Bot bot;

    public GameListener(Bot bot) {
        this.bot = bot;
    }

    /* Traduz as observacoes */
    private void parseObservations(String observations) {
        if (!observations.trim().equals("")) {
            // cria uma lista contendo a string de cada observacao
            String[] lista = observations.trim().split(",");
            String[] temp;

            // adiciona cada observacao de acordo com o nome no enum
            for (String o : lista) {
                // verificando a observacao de inimigo (enemy#X)
                temp = o.split("#");
                if (temp.length > 1) {
                    this.bot.ultimaObservacao.isInimigoFrente = true;
                    this.bot.ultimaObservacao.distanciaInimigoFrente = Integer.parseInt(temp[1]);
                }

                if (o.equals("blocked")) {
                    this.bot.ultimaObservacao.isParede = true;
                }
                if (o.equals("steps")) {
                    this.bot.ultimaObservacao.isInimigo = true;
                }
                if (o.equals("breeze")) {
                    this.bot.ultimaObservacao.isBuraco = true;
                }
                if (o.equals("flash")) {
                    this.bot.ultimaObservacao.isFlash = true;
                }
                if (o.equals("blueLight")) {
                    this.bot.ultimaObservacao.isTesouro = true;
                }
                if (o.equals("redLight")) {
                    this.bot.ultimaObservacao.isPowerup = true;
                }
            }
        }
    }


    /* Traduz o status do meu drone */
    private void parseStatus(String[] status) {
        if (status.length != 7) { return; }
        this.bot.x = Integer.parseInt(status[1]);
        this.bot.y = Integer.parseInt(status[2]);
        this.bot.dir = PlayerInfo.Direction.valueOf(status[3].toLowerCase());
        this.bot.state = PlayerInfo.State.valueOf(status[4].toLowerCase());
        this.bot.score = Long.parseLong(status[5]);
        this.bot.energy = Integer.parseInt(status[6]);
    }


    /* Traduz um player qualquer
      Neste caso, dir e state nao estao como string, mas como indices no enumerador
     */
    private void parsePlayer(String[] player) {
        if (player.length != 7) { return; }
        long node = Long.parseLong(player[1]);
        String name = player[2];
        int x = Integer.parseInt(player[3]);
        int y = Integer.parseInt(player[4]);
        PlayerInfo.Direction dir = PlayerInfo.Direction.values()[Integer.parseInt(player[5])];
        PlayerInfo.State state = PlayerInfo.State.values()[Integer.parseInt(player[6])];
        Color cor = Base.convertFromString(player[7]);

        PlayerInfo p = new PlayerInfo(node, name, x, y, dir, state, cor);
        this.bot.listaJogadores.put(node, p);
    }

    /* Atualiza o status do jogo */
    private void parseGameStatus(String[] status) {
        if (status.length != 3) { return; }
        PlayerInfo.State st = PlayerInfo.State.valueOf(status[1].toLowerCase());
        long time = Long.parseLong(status[2]);

        this.bot.state = st;
        this.bot.time = time;
    }

    /* Atualiza a scoreboard da batalha
      Cada scoreboard eh uma string com as informacoes separadas por # na forma:
      "nome#connected#score#energy(#cor)" */
    private void parseScoreboard(String[] scoreboard) {
        ArrayList<ScoreBoard> s = new ArrayList<>();
        for (int i = 1; i < scoreboard.length; i ++) {
            String[] ss = scoreboard[i].split("#");
            String name = ss[0];
            boolean connected = ss[1].equals("connected");
            int score = Integer.parseInt(ss[2]);
            int energy = Integer.parseInt(ss[3]);
            Color cor;
            if (ss.length == 5) {
                cor = Base.convertFromString(ss[4]);
            } else {
                cor = Color.BLACK;
            }

            ScoreBoard sb = new ScoreBoard(name, connected, score, energy, cor);
            s.add(sb);
        }
        this.bot.listaScores = s;
    }

    /* Traduz uma atualizacao do jogo */
    private void parseNotification(String notification) {
        this.bot.log.add(notification);
    }

    /* Traduz a entrada de um novo jogador */
    private void parsePlayerNew(String newPlayer) {
        String s = String.format("Player [%s] entrou no jogo!", newPlayer);
        this.bot.log.add(s);
    }

    /* Traduz a saida de um novo jogador */
    private void parsePlayerLeft(String leftPlayer) {
        String s = String.format("Player [%s] saiu do jogo!", leftPlayer);
        this.bot.log.add(s);
    }


    /* Traduz uma mudanca de nome */
    private void parseChangeName(String oldName, String newName) {
        String s = String.format("[%s] trocou de nome para [%s]", oldName, newName);
        this.bot.log.add(s);
    }

    /* Traduz um acerto de um disparo em um jogador */
    private void parseHit(String target) {
        String s = String.format("Acertei [%s]", target);
        this.bot.log.add(s);
        this.bot.ultimaObservacao.isAcerto = true;
    }

    /* Traduz um dano recebido devido a um disparo de um jogador */
    private void parseDamage(String shooter) {
        String s = String.format("Fui atingido por [%s]", shooter);

        this.bot.antiCheat(shooter);
        this.bot.ultimoAcerto = s;
        this.bot.ultimoTickAcerto = (int) System.currentTimeMillis();

        this.bot.log.add(s);
        this.bot.ultimaObservacao.isDano = true;
    }

    public void receiveCommand(String[] cmd) {

        Bot.ping = System.currentTimeMillis() - Bot.tickAtual;

        if (cmd[0].equals("o")) {
            if (cmd.length > 1) parseObservations(cmd[1]);
        }
        else if (cmd[0].equals("s")) parseStatus(cmd);
        else if (cmd[0].equals("player")) parsePlayer(cmd);
        else if (cmd[0].equals("g")) parseGameStatus(cmd);
        else if (cmd[0].equals("u")) parseScoreboard(cmd);
        else if (cmd[0].equals("notification")) parseNotification(cmd[1]);
        else if (cmd[0].equals("hello")) parsePlayerNew(cmd[1]);
        else if (cmd[0].equals("goodbye")) parsePlayerLeft(cmd[1]);
        else if (cmd[0].equals("changename")) parseChangeName(cmd[1], cmd[2]);
        else if (cmd[0].equals("h")) parseHit(cmd[1]);
        else if (cmd[0].equals("d")) parseDamage(cmd[1]);
    }
}
