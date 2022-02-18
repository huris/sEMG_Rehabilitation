using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Man : MonoBehaviour
{
    Animator anim;
    private float speed;
    private GameObject Canvas;
    public bool isChanging = false, isMovingStart = false;   

    public Slider slider;
    public Image sliderImage;
    // Start is called before the first frame update
    void Start()
    {
        anim = GetComponent<Animator>();
        Canvas = GameObject.Find("Canvas");
        //if(transform.parent == null)
        //{
        //    Canvas.transform.Find("leftlegChange").GetComponent<Slider>().onValueChanged.AddListener(ChangeLeg);
        //}

        slider = transform.Find("Canvas/Slider").GetComponent<Slider>();
        slider.onValueChanged.AddListener(ChangeLeg);

        sliderImage = transform.Find("Canvas/SliderImage").GetComponent<Image>();

        ManInit();
    }

    public void ManInit()
    {
        speed = 0;
        //Debug.Log(anim+this.gameObject.name);
        anim.SetFloat("test", speed);
        ChangeAll((slider.maxValue - slider.minValue) / 2);
    }

    // Update is called once per frame
    void Update()
    {    
        
    }

    public void ChangeLeg(float percent)
    {
        anim.Play(anim.GetCurrentAnimatorStateInfo(0).fullPathHash, 0, percent);
        sliderImage.fillAmount = percent / 2;
    }

    public void ChangeAll(float percent)
    {        
        anim.Play(anim.GetCurrentAnimatorStateInfo(0).fullPathHash, 0, percent);
        slider.value = percent;
        sliderImage.fillAmount = percent / 2;
    }

}
