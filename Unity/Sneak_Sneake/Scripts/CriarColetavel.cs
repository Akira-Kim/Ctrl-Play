using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CriarColetavel : MonoBehaviour
{

        public GameObject fruta;

        private Collider regiao;


    void Awake()
    {
        regiao = GameObject.Find("Cria coletavel").GetComponent<BoxCollider>();
    }

    void Start()
    {
        InvokeRepeating("Spawn", 3, 4);
    }

    void Spawn()
    {
        Vector3 posicao = new Vector3();
        posicao.x = Random.Range(regiao.bounds.min.x, regiao.bounds.max.x);
        ///y nao pode receber um numero aleatorio
        posicao.y = -3f;
        posicao.z = Random.Range(regiao.bounds.min.z, regiao.bounds.max.z);
        Instantiate(fruta, posicao, Quaternion.identity);
    }
}