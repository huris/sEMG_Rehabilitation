using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DataManager : MonoBehaviour
{

    public static DataManager instance = null;

    public List<float> LsEMGData = new List<float>();
    public List<float> RsEMGData = new List<float>();


    void Awake()
    {
        if (instance == null)
        {
            instance = this;
            //Debug.Log("@DataManager: Singleton created.");

        }
        else if (instance != this)
        {
            Destroy(gameObject);
        }

        DontDestroyOnLoad(this);
    }

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
