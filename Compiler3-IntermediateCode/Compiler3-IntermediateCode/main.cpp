//
//  main.cpp
//  Compiler3-IntermediateCode
//
//  Created by Vivian on 2017/12/6.
//  Copyright © 2017年 Vivian. All rights reserved.
//

#include<stdlib.h>
#include<fstream>
#include<iostream>
using namespace std;

#define MAX 100
int m=0,sum=0;//sum用于计算运算符的个数
//m用于标记输入表达式中字符的个数

char JG='A';
char str[MAX];//用于存输入表达式
int  token=0;//左括号的标志

/***********用于更改计算后数组中的值**************/
void change(int e)
{
    
    int f=e+2;
    char ch=str[f];
    if(ch>='A'&&ch<='Z')
    {
        for (int l=0; l<m+10; l++) {
            if(str[l]==ch)
                str[l]=JG;
        }
    }
    
    if(str[e]>='A'&&str[e]<='Z')
    {
        for(int i=0; i<m; i++)
        {
            if(str[i]==str[e])
                str[i]=JG;
        }
    }
    
}



void chengchuchuli(int i,int m)
{
    
    i++;
    for( ;i<=m-1;i++)//处理乘除运算
    {
        if(str[i]=='*'||str[i]=='/')
        {
            
            cout<<"("<<str[i]<<" "<<str[i-1]<<"  "<<str[i+1]<<"  "<<JG<<")"<<endl;
            change(i-1);
            str[i-1]=str[i]=str[i+1]=JG;
            sum--;
            JG=(char)(int)JG++;
        }
    }
}

void jiajianchuli(int j,int m)
{
    j++;
    for( ;j<=m-1;j++)//处理加减运算
    {
        if(str[j]=='+'||str[j]=='-')
        {
            cout<<"("<<str[j]<<" "<<str[j-1]<<"  "<<str[j+1]<<"  "<<JG<<")"<<endl;
            change(j-1);
            str[j-1]=str[j]=str[j+1]=JG;
            sum--;
            JG=(char)(int)JG++;
        }
        
    }
}

/*扫描一遍从文件中读入表达式*/
void scan(FILE *fin)
{
    int p[MAX];
    char ch='a';
    int c=-1,q=0;
    while(ch!=EOF)
    {
        ch=getc(fin);
        
        while(ch==' '||ch=='\n'||ch=='\t') ch=getc(fin);//消除空格和换行符
        
        str[m++]=ch;
        
        if(ch=='='||ch=='+'||ch=='-'||ch=='*'||ch=='/') sum++;
        
        else if(ch=='(')
        {
            p[++c]=m-1;
            
        }
        else if(ch==')')
        {
            q=m-1;
            chengchuchuli(p[c],q);//从左括号处理到又括号
            jiajianchuli(p[c],q);
            JG=(char)(int)JG--;
            str[p[c]]=str[m-1]=JG;
            c--;
            JG=(char)(int)JG++;
            
        }
    }
}

void sanyuanshi()
{
    
    for(int i=0;i<=m-1;i++)//处理乘除运算
    {
        if(str[i]=='*'||str[i]=='/')
        {
            
            cout<<"("<<str[i]<<"  "<<str[i-1]<<"  "<<str[i+1]<<"  "<<JG<<")"<<endl;
            change(i-1);
            str[i-1]=str[i]=str[i+1]=JG;
            sum--;
            JG=(char)(int)JG++;
        }
        
    }
    
    for(int j=0;j<=m-1;j++)//处理加减运算
    {
        if(str[j]=='+'||str[j]=='-')
        {
            
            cout<<"("<<str[j]<<"  "<<str[j-1]<<"  "<<str[j+1]<<"  "<<JG<<")"<<endl;
            change(j-1);
            str[j-1]=str[j]=str[j+1]=JG;
            sum--;
            JG=(char)(int)JG++;
        }
        
    }
    
    for(int k=0;k<=m-1;k++)//处理赋值运算
    {
        if(str[k]=='=')
        {
            
            JG=(char)(int)--JG;
            cout<<"("<<str[k]<<"  "<<str[k+1]<<"  "<<"  "<<" "<<str[k-1]<<")"<<endl;
            sum--;
            change(k+1);
            str[k-1]=JG;
        }
    }
    
}


int main(){
    char in[MAX]; //用于接收输入输出文件名
    FILE *fin; //用于指向输入输出文件的指针
    cout<<"请输入源程序文件名：";
    cin>>in;
    cout<<endl;
    if ((fin=fopen(in,"r"))==NULL) //判断输入文件名是否正确
    {
        cout<<endl<<"打开词法分析输入文件出错!"<<endl;
    }
    cout<<"四元式如下："<<endl;

    scan(fin);//调用函数从文件中读入表达式
    
    sanyuanshi();
    
    if(sum==0) cout<<"成功！"<<endl;
    else cout<<"有错误！"<<endl;
    
    //关闭文件
    fclose(fin);
    
}
