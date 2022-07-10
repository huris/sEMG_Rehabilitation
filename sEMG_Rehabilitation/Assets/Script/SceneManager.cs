using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SceneManager : MonoBehaviour
{
    public List<GameObject> mans;
    private int manindex=0;
    public bool canoperate = true;
    private CanvasController canvas;
    //public float DefaultPercent;
    // Start is called before the first frame update
    void Awake()
    {
        InitScene();
    }

    // Update is called once per frame
    void Update()
    {
        if (canoperate)
        {
            if (Input.GetKeyDown(KeyCode.A))
                SwitchMan(false);
            if (Input.GetKeyDown(KeyCode.D))
                SwitchMan(true);
        }
    }

    private void InitScene()
    {
        canvas = GetComponent<CanvasController>();
        //Slider slider = transform.Find("leftlegChange").GetComponent<Slider>();
        //DefaultPercent = (slider.maxValue-slider.minValue) / 2;
        mans = new List<GameObject>();
        mans.Add(GameObject.Find("man1"));
        mans.Add(GameObject.Find("man2"));
        mans.Add(GameObject.Find("man3"));
        mans.Add(GameObject.Find("man4"));
        for (int i = 0; i < mans.Count; i++)
            mans[i].SetActive(false);
        manindex = 0;
        mans[manindex].SetActive(true);
        canoperate = true;
    }

    private void SwitchMan(bool right)
    {
        int index = 0;
        if(right)
            index = (manindex + 1) % mans.Count;                   
        else        
            index = manindex - 1 < 0 ? mans.Count - 1 : manindex - 1;      
        canvas.FadeBackGround(mans[manindex], mans[index]);
        manindex = index;
    }
}
