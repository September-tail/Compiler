//
//  main.c
//  S_Scanner
//
//  Created by Vivian on 2017/11/27.
//  Copyright © 2017年 Vivian. All rights reserved.
//

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
char *Key[]={"begin","if","then","else","while","do","end","Const","Var","read","write"};//保留字
char *Opera[]={"+","-","*","/","=","<",">","(",")","{","}",",",";"};//标识符
int IsWord(char ch){//判断是否为字母
    if (((ch<='z')&&(ch>='a'))||((ch<='Z')&&(ch>='A'))){
        return 1;
    }
    else return 0;
}
int IsNum(char ch){//判断是否为数字
    if ((ch >= '0')&&(ch <= '9')) {
        return 1;
    }
    else return 0;
}
int IsKey(char *Word){//判断是否为保留字
    int m,i;
    for (i=0; i<11; i++) {
        if ((m=strcmp(Word, Key[i]))==0) {
            return 1;
        }
    }
    return 0;
}
int IsOpera(char *Word){//判断是否为标识符
    int m,i;
    for (i=0; i<13; i++) {
        if ((m=strcmp(Word, Opera[i]))==0) {
            return 1;
        }
    }
    return 0;
}
void Scanner(FILE *fp){
    char Word[100]={'\0'};
    char ch;
    int i,c;
    ch=fgetc(fp);
    if (IsWord(ch)) {
//        Word[0]=ch;
//        ch=fgetc(fp);
//        i=1;
        i=0;
        while (IsWord(ch)) {
            Word[i]=ch;
            i++;
            ch=fgetc(fp);
        }
        Word[i]='\0';
        fseek(fp, -1, 1);
        c=IsKey(Word);
        if (c==1) {
            printf("%s\t $Reserved words\n",Word);
        }
        else
            printf("%s\t &Identifier\n",Word);
    }
    else if (IsNum(ch)){
        Word[0]=ch;
        ch=fgetc(fp);
        i=1;
        while (IsNum(ch)) {
            Word[i]=ch;
            i++;
            ch=fgetc(fp);
        }
        Word[i]='\0';
        fseek(fp, -1, 1);
        printf("%s\t $Number\n",Word);
    }
    else{
        Word[0]=ch;
        printf("%s\n",Word);
    }
}

int main(){
    //char in[100];
    FILE *fp;
    char ch;
    if((fp=fopen("examplse\(输入\).txt","r"))==NULL)//打开操作
    {
        printf("The file can not be opened.\n");
        exit(1);//结束程序的执行
    }
    printf("\n********************Begin**********************\n\n");
    do{
        ch=fgetc(fp);
        if (ch=='#')
            break;
        else if(ch==' '||ch=='\t'||ch=='\n')
        {}
        else{
            fseek(fp, -1, 1);
            Scanner(fp);
        }
            
    }while (ch!='#');
    printf("\n********************End**********************\n\n");
    return 0;
}


