using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LMan : MonoBehaviour
{
    Animator anim;
    private float speed;
    private GameObject Canvas;
    public bool isChanging = false, isMovingStart = false;   

    public Slider slider;
    public Image sliderImage;

    public int FrameMax = 99;
    public int FrameMin = 0;
    public int PLUS = -1;
    public int Now = 0;
    public float Value = 0.0f;
    public BoxCollider footbox;

    // Start is called before the first frame update
    void OnEnable()
    {
        anim = GetComponent<Animator>();
        Canvas = GameObject.Find("Canvas");
        //if(transform.parent == null)
        //{
        //    Canvas.transform.Find("leftlegChange").GetComponent<Slider>().onValueChanged.AddListener(ChangeLeg);
        //}

        slider = transform.Find("Canvas/Slider").GetComponent<Slider>();
        sliderImage = transform.Find("Canvas/SliderImage").GetComponent<Image>();
        
        transform.Find("CanvasN/SpeedSlider").GetComponent<Slider>().onValueChanged.AddListener(delegate {
            SpeedSliderChange();
        });

        footbox = transform.Find("footbox").GetComponent<BoxCollider>();

        ManInit();
    }


    public void ManInit()
    {
        speed = 0.5f;
        //Debug.Log(anim+this.gameObject.name);
        anim.SetFloat("test", speed);
        ChangeAll((slider.maxValue - slider.minValue) / 2);

        FrameMax = 99;
        FrameMin = 0;
        PLUS = -1;
        Now = 0;
    }

    // Update is called once per frame
    void Update()
    {    
        
    }


    void FixedUpdate()
    {
        //print(Now);
        if (Now == FrameMax || Now == FrameMin)
        {
            PLUS = -PLUS;
        }
        Now += PLUS;
        Value = 1.0f * Now / (FrameMax - FrameMin + 1);
        slider.value = Value;
        sliderImage.fillAmount = Value / 2;

        // 测试用, 之后删
        DataManager.instance.LsEMGData.Add(Value);
        ChangeLeg(Value);
    }

    public void SpeedSliderChange()
    {
        FrameMax = (int)(300 - transform.Find("CanvasN/SpeedSlider").GetComponent<Slider>().value * 200);
        PLUS = -1;
        Now = 0;

        DataManager.instance.LsEMGData.Clear();
    }


    public void ChangeLeg(float percent)
    {
        anim.Play(anim.GetCurrentAnimatorStateInfo(0).fullPathHash, 0, percent);

        // 0 0 0;  0 0 -11.5;  1 1 1;  0.15 0.18 0.94;  0.2 0.2 0.3
        footbox.size = new Vector3(0.15f, 0.23f, -0.38f * percent * percent + 0.65f * percent + 0.08f);

        //sliderImage.fillAmount = percent / 2;
    }

    public void ChangeAll(float percent)
    {        
        anim.Play(anim.GetCurrentAnimatorStateInfo(0).fullPathHash, 0, percent);
        //slider.value = percent;
        //sliderImage.fillAmount = percent / 2;
    }

}
