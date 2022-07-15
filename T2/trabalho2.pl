/*
Arquivo de memoria:
folha -> Pergunta feita para saber se acertou o animal
galho -> Pergunta feita para reduzir as possibilidades de animais
pai -> gerencia relacao entre galhos e entre galho e folha
estrutura pai -> (no_pai,no_filho,resposta que liga o no_pai ao no_filho) 


Verifica se eh folha e se acertou ou errou
Se tiver errado pergunta qual era o animal
*/
resposta(X,Y,Z,File) :- (
						(folha(X), Y = sim, write("Eba acertei!"), nl, inicio(File));
						(folha(X), Y = nao, write("Droga errei :(  Qual animal pensou? Nao bote espaco"),nl,
							read(W),nl,
							/* Pega ultima palavra da folha, nome do animal e salva em K*/
							split_string(X," ","?",L), last(L,K),
							format("Qual pergunta devo fazer para distinguir '~a' de '~a'? Use aspas duplas para escrever com espaco",[W,K]),nl,
							read(I),nl,
							format("Agora digite qual a resposta certa para '~a' (sim / nao):",[W]),nl,
							read(J),nl,
							write("Obrigado por me ensinar algo novo!"),nl,
							/* Transforma arquivo em lista */
							file_to_list(File,List),
							/* Pega pai da folha */
							pai(U,X,Z),
							format(string(S),"pai(\"~a\",\"~a\",~a)",[U,X,Z]),
							/* Remove pai da lista, pois sera substituido */
							subtract(List,[S],T),
							/* Reescreve arquivo */
							rewrite(File, T, X, Z, W, I, J),
							/* Reinicia programa com o novo arquivo */
							inicio(File)
						)
					), !.

% main
/* 
Inicia o programa 
Carrega o File para a memoria
Realiza a primeira pergunta
*/
inicio(File) :- consult(File), pergunta("Eh um mamifero?", _, File).

% loop
/*
Realiza uma pergunta
X -> pergunta a ser realizada
Y -> resposta que levou a X
*/
pergunta(X, Y, File) :-  write(X),nl,
		write('q para sair.'),nl,
        write('Nao esqueca de finalizar sua resposta com . ex: sim. ou nao.'),nl,
        read(Z),
        nl,
		(
		/* Verifica se eh folha e se acertou ou errou */
		resposta(X,Z,Y,File);
			(
				/* Encerrar programa */
				(Z = 'q', write("ate breve!"), !, fail);
				/* 
				Nao eh folha 
				Pergunta filho em relacao a resposta dada
				*/
				(pai(X, W, Z), pergunta(W, Z, File),!)
			)
		).

/* Transforma um arquivo em lista */
file_to_list(FILE,LIST) :- 
   see(FILE), 
   inquire([],R), % gather terms from file
   reverse(R,LIST),
   seen.

inquire(IN,OUT):-
   read(Data), 
   (Data == end_of_file ->   % done
		OUT = IN 
        ;    % more
		(term_string(Data,Conv),
		inquire([Conv|IN],OUT) )) .

/* Separa o primeiro elemento da lista */
primeiro(X,Z, [X|Z]) :- !.

/* Termina de escrever no arquivo se lista ficar vazia */
finish_rewrite(L) :- L = [].

/* Apaga todo o conteudo do banco e escreve a nova primeira linha */
rewrite(File, List, X, Z, W, I, J) :- 
	   pai(K,X,Z),
	   inverso(J,O),
	   /* Cria novas linha para escrever no arquivo */
	   format(string(S1),"folha(\"Eh um ~a?\")",[W]),
	   format(string(S2),"galho(\"~a\")",[I]),
	   format(string(S3),"pai(\"~a\",\"~a\",~a)",[K,I,Z]),
	   format(string(S4),"pai(\"~a\",\"Eh um ~a?\",~a)",[I,W,J]),
	   format(string(S5),"pai(\"~a\",\"~a\",~a)",[I,X,O]),
	   append([[S1],[S2],[S3],[S4],[S5],List],L),
	   /* Ordena a lista de linhas */
	   sort(L,Sorted),
	   tell(File),      /* Abre arquivo escrevendo no começo, sobrescreve */ 
	   primeiro(First,Resto,Sorted),
	   (
			/* Transforma primeiro elem em string e escreve no arquivo */
			(
			string(First),
			format("~a.~n",[First])
			);
			(
			term_string(First,Conv),
			format("~a.~n",[Conv])
			)
		),
	   told,
	   /* Verifica se lista acabou */
	   (finish_rewrite(Resto); rewrite_cont(File,Resto)),!.

rewrite_cont(File, List) :- 
       append(File),      /* Abre arquivo e escreve no final */ 
	   primeiro(First,Resto,List),
	   (
			/* Transforma primeiro elem em string e escreve no arquivo */
			(
			string(First),
			format("~a.~n",[First])
			);
			(
			term_string(First,Conv),
			format("~a.~n",[Conv])
			)
		),
	   told,
	   /* Verifica se lista acabou */
	   (finish_rewrite(Resto); rewrite_cont(File,Resto)), !.

/* inverte sim e nao */ 
inverso(sim,nao).
inverso(nao,sim).