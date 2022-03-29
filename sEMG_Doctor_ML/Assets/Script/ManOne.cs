using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.Serialization;
using System.Text;
using System.Threading;


public class ManOne : MonoBehaviour
{
    Man rightman;
    Man leftman;

    // 左右按钮
    public Transform LMove;
    public bool isLMove;

    public Transform RMove;
    public bool isRMove;


    // 通信
    private string message;
    private string end_tag = Encoding.UTF8.GetString(Encoding.UTF8.GetBytes("exit"));
    private Socket client;
    private string host = "127.0.0.1";
    private int port = 10086;
    private byte[] messTmp = new byte[1024];
    public int cnt = 0;

    void Start()
    {
        // 构建一个Socket实例，并连接指定的服务端。这里需要使用IPEndPoint类(ip和端口号的封装)
        client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        try
        {
            client.Connect(new IPEndPoint(IPAddress.Parse(host), port));
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
            return;
        }

        if (DataManager.instance.sEMGData == null)
        {
            DataManager.instance.sEMGData = new List<float>();
        }
        else
        {
            DataManager.instance.sEMGData.Clear();
        }
    }

    // Start is called before the first frame update
    void OnEnable()
    {
        rightman = transform.Find("manright").GetComponent<Man>();
        leftman = transform.Find("manleft").GetComponent<Man>();

        LMove = transform.Find("Canvas/LMove");
        isLMove = true;

        RMove = transform.Find("Canvas/RMove");
        isRMove = true;
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void FixedUpdate()
    {
        //GetMessage();
    }

    public void isLMoveButtonChange()
    {
        if (isLMove)
        {
            LMove.GetComponent<Image>().color = new Color32(38, 255, 68, 195);
            LMove.GetChild(0).GetComponent<Text>().text = "Left Move";

            isLMove = false;
            leftman.gameObject.SetActive(false);
        }
        else
        {
            LMove.GetComponent<Image>().color = new Color32(248, 46, 32, 204);
            LMove.GetChild(0).GetComponent<Text>().text = "Left Stop";

            isLMove = true;
            leftman.gameObject.SetActive(true);
        }
    }

    public void isRMoveButtonChange()
    {
        if (isRMove)
        {
            RMove.GetComponent<Image>().color = new Color32(38, 255, 68, 195);
            RMove.GetChild(0).GetComponent<Text>().text = "Right Move";

            isRMove = false;
            rightman.gameObject.SetActive(false);
        }
        else
        {
            RMove.GetComponent<Image>().color = new Color32(248, 46, 32, 204);
            RMove.GetChild(0).GetComponent<Text>().text = "Right Stop";

            isRMove = true;
            rightman.gameObject.SetActive(true);
        }
    }



    void OnDestroy()
    {
        SendOver(true);
        client.Close();
    }

    public void ChangeRightLeg(float percent)
    {
        rightman.ChangeAll(percent);
    }

    public void ChangeLeftLeg(float percent)
    {
        leftman.ChangeAll(percent);
    }

    void GetMessage()
    {
        client.Receive(messTmp);

        message = Encoding.UTF8.GetString(messTmp);

        //print(message);

        float value = float.Parse(message);

        DataManager.instance.sEMGData.Add(value);
            
        ChangeRightLeg(value);
        ChangeLeftLeg(value);


        SendOver(false);
    }

    void SendOver(bool isExit)
    {
        byte[] buffer;
        if (isExit)
        {
            // 发一个2说明退出程序
            buffer = Encoding.UTF8.GetBytes("2");
        }
        else
        {
            buffer = Encoding.UTF8.GetBytes("1");
        }
        client.Send(buffer);
    }
}
