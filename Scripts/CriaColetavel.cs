using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CriaColetavel : MonoBehaviour
{
    public GameObject fruta;
    public Collider regiaop;
    // Start is called before the first frame update
    void Start()
    {
        InvokeRepeating("Spawn", 3, 4);
    }

    // Update is called once per frame
    void Update()
    {
       
    }

    void Spawn()
{
        Vector3 posicao = new Vector3();
        posicao.x = Random.Range(regiaop.bounds.min.x, regiaop.bounds.max.x);
        //Y nao pode receber posição aleatoria
        posicao.y = 0.6f;
        posicao.z = Random.Range(regiaop.bounds.min.z, regiaop.bounds.max.z);
        Instantiate(fruta, posicao, Quaternion.identity);
    }
}
