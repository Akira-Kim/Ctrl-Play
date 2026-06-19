using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class Movimento : MonoBehaviour
{
    public float moveSpeed = 5;
    public float direcaoSpeed = 180;
    public float bodySpeed = 5;
    public int gap = 10;

    private GameManager controladorJogo;

    public GameObject bodyPrefab;

    private List<GameObject> bodyParts = new List<GameObject>();
    private List<Vector3> positionsHistory = new List<Vector3>();

    private AudioSource audioSource;
    public AudioClip collectsound;

    private bool morreu = false;

    private float tempoDeVida = 0f;
    public float tempoProtecao = 0.3f;

    void Start()
    {
        GameObject controlador = GameObject.Find("Controlador");

        if (controlador != null)
            controladorJogo = controlador.GetComponent<GameManager>();

        audioSource = GetComponent<AudioSource>();

        positionsHistory.Add(transform.position);

        // 🔥 SPAWN CORRETO (NUNCA AFUNDA)
        Collider headCol = GetComponent<Collider>();
        Collider bodyColPrefab = bodyPrefab.GetComponent<Collider>();

        float distancia = 1.8f;

        Vector3 spawnPos = transform.position - transform.forward * distancia;

        if (headCol != null && bodyColPrefab != null)
        {
            float baseCabeca = headCol.bounds.min.y;
            float alturaCorpo = bodyColPrefab.bounds.extents.y;

            spawnPos.y = baseCabeca + alturaCorpo + 0.02f;
        }
        else
        {
            spawnPos.y = transform.position.y + 0.5f;
        }

        GameObject firstBody = Instantiate(bodyPrefab, spawnPos, transform.rotation);
        bodyParts.Add(firstBody);

        // 🔥 ignora colisão inicial
        Collider bodyCol = firstBody.GetComponent<Collider>();
        if (headCol != null && bodyCol != null)
        {
            Physics.IgnoreCollision(headCol, bodyCol);
        }
    }

    void Update()
    {
        if (morreu) return;

        tempoDeVida += Time.deltaTime;

        // Movimento
        transform.position += transform.forward * moveSpeed * Time.deltaTime;

        // Input
        float direcionar = 0f;

        if (Keyboard.current.aKey.isPressed || Keyboard.current.leftArrowKey.isPressed)
            direcionar = -1f;

        if (Keyboard.current.dKey.isPressed || Keyboard.current.rightArrowKey.isPressed)
            direcionar = 1f;

        transform.Rotate(Vector3.up * direcionar * direcaoSpeed * Time.deltaTime);

        // Histórico
        positionsHistory.Insert(0, transform.position);

        int index = 1;

        foreach (var body in bodyParts)
        {
            Vector3 point = positionsHistory[
                Mathf.Clamp(index * gap, 0, positionsHistory.Count - 1)
            ];

            Vector3 moveDirection = point - body.transform.position;
            body.transform.position += moveDirection * bodySpeed * Time.deltaTime;

            body.transform.LookAt(point);

            index++;
        }
    }

    private void GrowSnake()
    {
        if (bodyParts.Count == 0) return;

        GameObject lastBodyPart = bodyParts[bodyParts.Count - 1];

        Vector3 newPosition =
            lastBodyPart.transform.position -
            lastBodyPart.transform.forward * 1.5f;

        newPosition.y = transform.position.y + 0.02f;

        GameObject body = Instantiate(bodyPrefab, newPosition, Quaternion.identity);
        bodyParts.Add(body);
    }

    private void GameOver()
    {
        if (morreu || tempoDeVida < tempoProtecao) return;

        morreu = true;

        moveSpeed = 0;
        direcaoSpeed = 0;

        if (controladorJogo != null)
            controladorJogo.FimDeJogo();

        Destroy(gameObject);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("food"))
        {
            GrowSnake();

            if (controladorJogo != null)
                controladorJogo.pontuacao++;

            if (audioSource != null && collectsound != null)
                audioSource.PlayOneShot(collectsound);

            Destroy(other.gameObject);
        }

        if (other.CompareTag("borda") ||
            other.CompareTag("corpo") ||
            other.CompareTag("Wall"))
        {
            GameOver();
        }
    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("borda") ||
            collision.gameObject.CompareTag("corpo") ||
            collision.gameObject.CompareTag("Wall"))
        {
            GameOver();
        }
    }
}