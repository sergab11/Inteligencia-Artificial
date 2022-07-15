package control.map;

import INF1771_GameClient.Dto.PlayerInfo;
import control.enums.Action;
import control.enums.Position;

import java.util.ArrayList;
import java.util.HashMap;

/* Classe para a A* */
class ASearch {

    private static HashMap<String, ASearch> hashMap;

    public static ASearch getNode(int x, int y, PlayerInfo.Direction dir) {
        return getNode(x, y, dir, false);
    }
    public static ASearch getNode(int x, int y, PlayerInfo.Direction dir, boolean ehAtras) {
        String s = x + "/" + y + "/" + dir + "/" + ehAtras;
        if (hashMap.containsKey(s)) { return hashMap.get(s); }
        ASearch n = new ASearch(x, y, dir, ehAtras);
        hashMap.put(s, n);
        return n;
    }

    public static void init() {hashMap = new HashMap<>();}

    public int distanciaFinal;
    public int ticksPercorridos = 1000000;
    public ASearch anterior;

    public int x;
    public int y;
    public boolean ehAtras;
    public boolean ehSafe;

    public PlayerInfo.Direction dir;
    public ASearch(int x, int y, PlayerInfo.Direction dir) {
        this.x = x; this.y = y; this.dir = dir; ehAtras = false;
        this.ehSafe = Field.get(x, y) == Position.SEGURO;
    }
    public ASearch(int x, int y, PlayerInfo.Direction dir, boolean ehAtras) {
        this.x = x; this.y = y; this.dir = dir; this.ehAtras = ehAtras;
    }

    /* Gera os vizinhos para o algoritmo do A*
      Retira Nodes invalidos */
    public ASearch[] gerarVizinhos(ASearch n) {
        ASearch[] ret;
        switch (n.dir) {
            case north -> ret = new ASearch[] {
                    ASearch.getNode(x, y - 1, dir), ASearch.getNode(x, y + 1, dir, true),
                    ASearch.getNode(x, y, PlayerInfo.Direction.east),
                    ASearch.getNode(x, y, PlayerInfo.Direction.west),
            };
            case south -> ret = new ASearch[] {
                    ASearch.getNode(x, y + 1, dir), ASearch.getNode(x, y - 1, dir, true),
                    ASearch.getNode(x, y, PlayerInfo.Direction.east),
                    ASearch.getNode(x, y, PlayerInfo.Direction.west)
            };
            case east -> ret = new ASearch[] {
                    ASearch.getNode(x + 1, y, dir), ASearch.getNode(x - 1, y, dir, true),
                    ASearch.getNode(x, y, PlayerInfo.Direction.north),
                    ASearch.getNode(x, y, PlayerInfo.Direction.south)
            };
            case west -> ret = new ASearch[] {
                    ASearch.getNode(x - 1, y, dir), ASearch.getNode(x + 1, y, dir, true),
                    ASearch.getNode(x, y, PlayerInfo.Direction.north),
                    ASearch.getNode(x, y, PlayerInfo.Direction.south)
            };
            default -> ret = null;
        }
        int x, y;
        for (int i = 0; i < 4; i ++) {
            x = ret[i].x;
            y = ret[i].y;
            Position tipo = Field.get(x, y);
            if (tipo == Position.PERIGO || tipo == Position.PAREDE || tipo == Position.DESCONHECIDO) {
                ret[i] = null;
            }
        }
        return ret;
    }

    public Path gerarCaminho() {
        ASearch atual = this;
        ASearch anterior = this.anterior;

        ArrayList<Action> acoes = new ArrayList<>();
        while (anterior != null) {
            if (atual.dir == anterior.dir) {
                switch (atual.dir) {
                    case north -> {
                        if (atual.y > anterior.y) { 
                        	acoes.add(0, Action.TRAS); 
                        } else { 
                        	acoes.add(0, Action.FRENTE); 
                        }
                    }
                    case south -> {
                        if (atual.y < anterior.y) { 
                        	acoes.add(0, Action.TRAS); 
                        } else { 
                        	acoes.add(0, Action.FRENTE); 
                        }
                    }
                    case west -> {
                        if (atual.x > anterior.x) { 
                        	acoes.add(0, Action.TRAS); 
                        } else { 
                        	acoes.add(0, Action.FRENTE); 
                        }
                    }
                    case east -> {
                        if (atual.x < anterior.x) { 
                        	acoes.add(0, Action.TRAS); 
                        } else { 
                        	acoes.add(0, Action.FRENTE); 
                        }
                    }
                }
            } else {
                switch (atual.dir) {
                    case north -> {
                        if (anterior.dir == PlayerInfo.Direction.east) {
                        	acoes.add(0, Action.ESQUERDA);
                        } else { 
                        	acoes.add(0, Action.DIREITA);
                        }
                    }
                    case south -> {
                        if (anterior.dir == PlayerInfo.Direction.west) {
                        	acoes.add(0, Action.ESQUERDA);
                        } else { 
                        		acoes.add(0, Action.DIREITA);
                        }
                    }
                    case east -> {
                        if (anterior.dir == PlayerInfo.Direction.south) {
                        	acoes.add(0, Action.ESQUERDA);
                        } else {
                        	acoes.add(0, Action.DIREITA);
                        }
                    }
                    case west -> {
                        if (anterior.dir == PlayerInfo.Direction.north) {
                        	acoes.add(0, Action.ESQUERDA);
                        } else { 
                        	acoes.add(0, Action.DIREITA);
                        }
                    }
                }
            }
            atual = anterior;
            anterior = atual.anterior;
        }

        if (acoes.size() == 0) { return null; }

        Path ret = new Path();
        ret.xDest = this.x;
        ret.yDest = this.y;

        ret.acoes = new Action[acoes.size()];
        for (int i = 0; i < acoes.size(); i ++) { ret.acoes[i] = acoes.get(i); }
        ret.tamanho = ret.acoes.length;
        return ret;
    }
}