#pragma once

#include<cstdio>
#include<cstring>
#include<iostream>
#include<utility>
using namespace std;

const int SIZE = 1e5;

char ch;
int row = 1, col = 0, tcol = 0;

char t[][20] = { "Error","关键字","分界符","算术运算符","关系运算符","无符号数","标识符" };

//关键字表
char k[SIZE][80] = { "do","end","for","if","print","scanf","then","while"};


//分界符表（算术运算符和关系运算符也在里面）
char s[3][SIZE][5] = { {";",",","(",")","[","]","{","}" },
					   {"+","-","*","/" },
					   {"<","<=","=",">",">=","<>"} };

// 标识符表
struct ID {
	char dat[SIZE][80];
	int len = 0;
}id;

//常数表
struct CI {
	char dat[SIZE][80];
	int len = 0;
}ci;

char instring[80]; //单词缓存


//跳过空白符，直至读入一个非空白符到ch
char getBC() {
	int ch ;
	while (ch = getchar()) {
		if (ch != ' ' && ch != '\t' && ch != '\n' && ch != EOF) {
			//cout << ch << endl;
			col++;
			tcol = col;
			return ch;
		}
		else if (ch == '\n') row++, col = 0;
		else if (ch == ' ') col++;
		else if (ch == '\t') col += 4;
		else if (ch == EOF) exit(0);
	}
}

//把下一个字符读入到ch，记录行、列数
char  getChar() {
	int ch = getchar();
	if (ch == '\n') {
		row++, col = 0;
	}
	else if (ch == '\t') col += 4;
	else if (ch == EOF) exit(0);
	else col++;
	return ch;
}

//判断字母、下划线
bool isLetter(char ch) {
	return ('a' <= ch && ch <= 'z') || ('A' <= ch && ch <= 'Z') || (ch == '_');
}

//判断数字
bool isDigit(char ch) {
	return '0' <= ch && ch <= '9';
}

//查找保留字
int reserveWord() {
	int i = 0;
	while( k[i][0] != '\0' && strcmp(instring,k[i]) != 0 ){
		i++;
	}
	if (k[i][0] == '\0') {
		return 0;
	}
	else return i;
}

//查找标识符
int idWord() {
	int i = 0;
	while (i < id.len) {
		if (strcmp(instring, id.dat[i]) == 0) {
			return i + 1;
		}
		i++;
	}
	return 0;
}

//插入标识符
int insertID() {
	strcpy(id.dat[id.len++], instring);
	return id.len;
}

//查找分界符
int  delimiterWord(char *instring) {
	int i = 0;
	while (s[0][i][0] != '\0' && strcmp(instring, s[0][i]) != 0) {
		i++;
	}
	if (s[0][i][0] == '\0') {
		return 0;
	}
	else return i+1;
}

//查找算术运算符
int a_operator(char *instring) {
	int i = 0;
	while (s[1][i][0] != '\0' && strcmp(instring, s[1][i]) != 0) {
		i++;
	}
	if (s[1][i][0] == '\0') {
		return 0;
	}
	else return i+1;
}

//查找关系运算符
int r_operator(char *instring) {
	int i = 0;
	while (s[2][i][0] != '\0' && strcmp(instring, s[2][i]) != 0) {
		i++;
	}
	if (s[2][i][0] == '\0') {
		return 0;
	}
	else return i+1;
}

//判断无符号数
bool isConst( ) {
	int point = 0;
	for (int i = 0; instring[i]; ++i) {
		if (!isDigit(instring[i]) && instring[i]!='.') {
			return false;
		}
		if (instring[i] == '.' ) {
			if (point == 1 || instring[i + 1] == '\0') return false;
			else point = 1;
		}
	}
	return true;
}

//查无符号数表
int findConst() {
	for (int i = 0; i < ci.len; ++i) {
		if (strcmp(ci.dat[i], instring) == 0) {
			return i + 1;
		}
	}
	return 0;
}

//插入无符号数
int insertConst() {
	strcpy(ci.dat[ci.len++],instring);
	return ci.len ;
}

//搜索指针回调一个字符位置
void restract() {
	fseek(stdin, -1, SEEK_CUR);
	if (col) col--;
}

//错误处理
void errorProcess(int &type,int &pointer) {
	type = 0, pointer = 0;
}

//输出信息
void Print(int type,int pointer) {
	if (type != 0) {
		printf("%-20s(%d,%d)\t\t%-20s(%d,%d)\n", instring, type, pointer, t[type], row, tcol);
	}
	else {
		printf("%-20s%-12s\t%-20s(%d,%d)\n", instring, t[type],t[type], row, tcol);
	}
}

void solve() {
	printf("单词\t\t二元序列\t\t类型\t\t位置（行，列）\n");
	int type=0, pointer=0;
	while (ch = getBC() ) {
		//cout << ch << endl;
		if (isLetter(ch)) {//关键字,标识符
			int pos = 0;
			while (isLetter(ch) || isDigit(ch)) {
				instring[pos++] = ch;
				ch = getChar();
			}
			instring[pos] = '\0';
			//cout << instring << endl;
			if ((pointer = reserveWord()) != 0) {
				type = 1;
			}
			else {
				type = 6;
				if ((pointer = idWord()) == 0) {
					pointer = insertID();
				}
			}
			restract();
		}
		else if (isDigit(ch)) {//无符号数
			int pos = 0;
			while (isLetter(ch) || isDigit(ch)||ch=='.') {
				instring[pos++] = ch;
				ch = getChar();
			}
			instring[pos] = '\0';
			//cout << instring << endl;
			if (isConst( )) {
				type = 5;
				if ((pointer = findConst()) == 0) {
					pointer = insertConst();
				}
			}
			else errorProcess(type, pointer);

			restract();
		}
		else { //运算符，分界符
			int pos = 0;
			instring[pos++] = ch;
			instring[pos] = '\0';
			char temp_s[2];
			if ((pointer = a_operator(instring)) != 0) { //算术运算符
				type = 3;
				temp_s[0] = getChar();
				temp_s[1] = '\0';
				while (a_operator(temp_s) != 0) {
					instring[pos++] = temp_s[0];
					temp_s[0] = getChar();
					temp_s[1] = '\0';
				}
				instring[pos] = '\0';
				restract();
				if (a_operator(instring) == 0) {
					errorProcess(type,pointer);
				}
				//cout << instring << endl;
			}
			else if ((pointer = r_operator(instring)) != 0) {//关系运算符
				type = 4;
				temp_s[0] = getChar();
				temp_s[1] = '\0';
				while (r_operator(temp_s) != 0) {
					instring[pos++] = temp_s[0];
					temp_s[0] = getChar();
					temp_s[1] = '\0';
				}
				instring[pos] = '\0';
				restract();
				if (r_operator(instring) == 0) {
					errorProcess(type, pointer);
				}
				//cout << instring << endl;
			}
			else if ((pointer = delimiterWord(instring)) != 0) {//分界符
				type = 2;
				//cout << instring << endl;
			}
			else errorProcess(type,pointer);
		}
		Print(type, pointer);
	}
}