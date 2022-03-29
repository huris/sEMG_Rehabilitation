using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public class collsionMonitor : MonoBehaviour
{
    private Rigidbody rgd;
    public float speed;
    public float force;
    public float wallforce;
    public float footforce;
    public float dec;
    public bool willLaunch;

    void OnEnable()
    {
        rgd = GetComponent<Rigidbody>(); //获取球体上的刚体组件
        wallforce = -9f;
        footforce = 15f;
        force = wallforce;
        speed = force;
        dec = 0.001f;
        willLaunch = false;
    }

    void Update()
    {
        //float h = Input.GetAxis("Horizontal");//水平方向 对应← →
        //float v = Input.GetAxis("Vertical"); //垂直方向 对应↑ ↓ 
        ////rgd.AddForce(new Vector3(h, 0, v) * speed);//给刚体施加一个力就可以运动了,添加一个方向即可

        //print(force);

        if (willLaunch)
        {
            if(DataManager.instance.sEMGData.Last() > 0.5f)
            {
                int num = DataManager.instance.sEMGData.Count;
                int n = Mathf.Min(5, num);
                while(n > 1)
                {
                    if (DataManager.instance.sEMGData[num - n] > DataManager.instance.sEMGData[num - n + 1])
                    {
                        print(DataManager.instance.sEMGData[num - n] + " " + DataManager.instance.sEMGData[num - n + 1]);
                        break;
                    }
                    n--;
                }
                if(n == 1)
                {
                    force = footforce;
                    speed = force;
                    dec = -dec;
                    willLaunch = false;
                }
            }
        }else
        {
            rgd.AddForce(new Vector3(0, 0, force + speed - dec));
        }
    }

    void OnCollisionEnter(Collision collision) {
        //Debug.Log("Name is " + name);

        if (collision.collider.name == "wall") {
            //rgd.AddForce(new Vector3(0, 0, force));
            force = wallforce;
            speed = force;
            dec = -dec;
        } else if(collision.collider.name == "footbox")
        {
            willLaunch = true;
        }

    }
}
