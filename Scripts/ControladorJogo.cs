using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.SceneManagement;


public class ControladorJogo : MonoBehaviour
{
    //Variável booleana (verdadeiro ou falso) que indica se o jogo está rodando ou não
    public bool jogando;

    //Objeto inteiros da cena que devem aparecer ou desaparecer em determinados momentos
    public GameObject painelMenu,painelFim;


    //Componentes de Texto dos objetos que indicam os segundos e minutos do jogo
    public TMP_Text pontuacaoTxt, pontuacaoFinal;

    //Variável auxiliar que conta o tempo de partida
    float tempo;


    //Variável para guardar os pontos ao colidir
    public int pontuacao;

    void Start()
    {
        //A partida começou
        jogando = true;

        //Congelando o jogo para funcionamento do painel menu
        Time.timeScale = 0f;

    }

    void Update()
    {
        //Se a booleana jogando é verdadeira, o jogo está rodando
        if (jogando)
        {
            //Se o jogo está rodando, o tempo de partida deve ser contado
            //A variável auxiliar conta o tempo por inteiro
            //tempo += Time.deltaTime;

           

            //Convertendo o valor da pontuacao para string e atribuindo ao componente Text da cena
            pontuacaoTxt.text = pontuacao.ToString("00");
        }
    }

    public void Pause()
    {
        if (jogando)
        {

            //Atualiza a booleana jogando para false
            jogando = false;

            //Atualiza a escala de tempo congela
            Time.timeScale = 0f;

           

            //Desativa o objeto pontos
           // pontos.SetActive(false);

        }
        else
        {
            //Atualiza a booleana jogando para true
            jogando = true;

            //A escala de tempo volta ao normal
            Time.timeScale = 1f;
            

            //Desativa o objeto pontos
            //pontos.SetActive(true);
        }
    }

    public void Iniciar()
    {
     
        //Desabilitando o painel do menu
        painelMenu.SetActive(false);
        //pontos.SetActive(true);

        //Atualiza a escala de tempo para 1, fazendo
        //o jogo rodar em sua velocidade normal
        Time.timeScale = 1f;
    }

    public void FimDeJogo()
    {
        //Atualiza a booleana jogando para false para indicar a todos que o jogo não está rodando
        jogando = false;

        //Ativa o painél de Game Over para que este apareça na tela
        painelFim.SetActive(true);


        pontuacaoFinal.text = pontuacao.ToString("00");
    }
    public void Reiniciar()
    {
        //Chamada da cena 0 (cena atual)
        SceneManager.LoadScene(0);
    }

}
