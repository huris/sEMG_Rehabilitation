using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.Serialization;
using System.Text;
using System.Threading;
using UnityEngine;

public class Py2Unity : MonoBehaviour
{

    private string message;
    private string end_tag = Encoding.UTF8.GetString(Encoding.UTF8.GetBytes("exit"));
    private Socket client;
    private string host = "127.0.0.1";
    private int port = 10086;
    private byte[] messTmp = new byte[1024];
    public int cnt = 0;

    // Use this for initialization
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

    }

    void GetMessage()
    {
        client.Receive(messTmp);

        message = Encoding.UTF8.GetString(messTmp);

        print(message);

        SendOver(false);
    }

    void SendOver(bool isExit)
    {
        byte[] buffer;
        if (isExit)
        {
            buffer = Encoding.UTF8.GetBytes("0");
        }
        else
        {
            buffer = Encoding.UTF8.GetBytes("1");
        }
        client.Send(buffer);
    }

    void OnDestroy()
    {
        SendOver(true);
        client.Close();
    }

    void FixedUpdate()
    {
        GetMessage();
    }
}
