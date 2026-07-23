using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{

    //Variável booleana (verdadeiro ou falso) que indica se o jogo está rodando ou não
    public bool jogando;

    //Objeto inteiros da cena que devem aparecer ou desaparecer em determinados momentos
    public GameObject painelMenu, painelFim;

    //Componentes de Texto dos objetos que indicam os segundos e minutos do jogo
    public TMP_Text pontuacaoTxt, pontuacaoFinal;

    public int pontuacao;

    void Start()
    {
        //A partida começou
        jogando = true;

        //Congelando o jogo para funcionamento do painel menu
        Time.timeScale = 0f;

    }

    // Update is called once per frame
    void Update()
    {
        //Convertendo o valor da pontuacao para string e atribuindo ao componente Text da cena
        pontuacaoTxt.text = pontuacao.ToString("00");
    }

    public void Iniciar()
    {

        //Desabilitando o painel do menu
        painelMenu.SetActive(false);

        //Atualiza a escala de tempo para 1, fazendo
        //o jogo rodar em sua velocidade normal
        Time.timeScale = 1f;
    }

    public void FimDeJogo()
    {
        //Atualiza a booleana jogando para false para
        //indicar a todos que o jogo não está rodando
        jogando = false;

        //Ativa o painél de Game Over para que este apareça na tela
        painelFim.SetActive(true);

        //Convertendo o valor da pontuacao para string e atribuindo
        //ao componente Text da cena
        pontuacaoFinal.text = pontuacao.ToString("00");
    }

    public void Reiniciar()
    {
        //Chamada da cena 0 (cena atual)
        SceneManager.LoadScene(0);
    }
}
