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
        rgd = GetComponent<Rigidbody>(); //��ȡ�����ϵĸ������
        force = -7f;
        speed = force;
        dec = 0.001f;
    }

    void Update()
    {
        //float h = Input.GetAxis("Horizontal");//ˮƽ���� ��Ӧ�� ��
        //float v = Input.GetAxis("Vertical"); //��ֱ���� ��Ӧ�� �� 
        ////rgd.AddForce(new Vector3(h, 0, v) * speed);//������ʩ��һ�����Ϳ����˶���,���һ�����򼴿�

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
