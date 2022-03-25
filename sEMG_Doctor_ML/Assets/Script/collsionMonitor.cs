using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class collsionMonitor : MonoBehaviour
{
    private Rigidbody rgd;
    public float speed;
    public float force;
    public float dec;

    void Start()
    {
        rgd = GetComponent<Rigidbody>(); //获取球体上的刚体组件
        force = -7f;
        speed = force;
        dec = 0.001f;
    }

    void Update()
    {
        //float h = Input.GetAxis("Horizontal");//水平方向 对应← →
        //float v = Input.GetAxis("Vertical"); //垂直方向 对应↑ ↓ 
        ////rgd.AddForce(new Vector3(h, 0, v) * speed);//给刚体施加一个力就可以运动了,添加一个方向即可

        //print(force);

        rgd.AddForce(new Vector3(0, 0, force + speed - dec));
    }

    void OnCollisionEnter(Collision collision) {
        //Debug.Log("Name is " + name);

        if (collision.collider.name == "wall" || collision.collider.name == "footbox") {
            //rgd.AddForce(new Vector3(0, 0, force));
            force = -force;
            speed = force;
            dec = -dec;
        }

    }
}
