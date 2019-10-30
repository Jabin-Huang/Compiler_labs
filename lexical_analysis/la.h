#pragma once

#include<cstdio>
#include<cstring>
#include<iostream>
#include<utility>
using namespace std;

const int SIZE = 1e5;

char ch;
int row = 1, col = 0, tcol = 0;

char t[][20] = { "Error","�ؼ���","�ֽ��","���������","��ϵ�����","�޷�����","��ʶ��" };

//�ؼ��ֱ�
char k[SIZE][80] = { "do","end","for","if","print","scanf","then","while"};


//�ֽ��������������͹�ϵ�����Ҳ�����棩
char s[3][SIZE][5] = { {";",",","(",")","[","]","{","}" },
					   {"+","-","*","/" },
					   {"<","<=","=",">",">=","<>"} };

// ��ʶ����
struct ID {
	char dat[SIZE][80];
	int len = 0;
}id;

//������
struct CI {
	char dat[SIZE][80];
	int len = 0;
}ci;

char instring[80]; //���ʻ���


//�����հ׷���ֱ������һ���ǿհ׷���ch
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

//����һ���ַ����뵽ch����¼�С�����
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

//�ж���ĸ���»���
bool isLetter(char ch) {
	return ('a' <= ch && ch <= 'z') || ('A' <= ch && ch <= 'Z') || (ch == '_');
}

//�ж�����
bool isDigit(char ch) {
	return '0' <= ch && ch <= '9';
}

//���ұ�����
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

//���ұ�ʶ��
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

//�����ʶ��
int insertID() {
	strcpy(id.dat[id.len++], instring);
	return id.len;
}

//���ҷֽ��
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

//�������������
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

//���ҹ�ϵ�����
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

//�ж��޷�����
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

//���޷�������
int findConst() {
	for (int i = 0; i < ci.len; ++i) {
		if (strcmp(ci.dat[i], instring) == 0) {
			return i + 1;
		}
	}
	return 0;
}

//�����޷�����
int insertConst() {
	strcpy(ci.dat[ci.len++],instring);
	return ci.len ;
}

//����ָ��ص�һ���ַ�λ��
void restract() {
	fseek(stdin, -1, SEEK_CUR);
	if (col) col--;
}

//������
void errorProcess(int &type,int &pointer) {
	type = 0, pointer = 0;
}

//�����Ϣ
void Print(int type,int pointer) {
	if (type != 0) {
		printf("%-20s(%d,%d)\t\t%-20s(%d,%d)\n", instring, type, pointer, t[type], row, tcol);
	}
	else {
		printf("%-20s%-12s\t%-20s(%d,%d)\n", instring, t[type],t[type], row, tcol);
	}
}

void solve() {
	printf("����\t\t��Ԫ����\t\t����\t\tλ�ã��У��У�\n");
	int type=0, pointer=0;
	while (ch = getBC() ) {
		//cout << ch << endl;
		if (isLetter(ch)) {//�ؼ���,��ʶ��
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
		else if (isDigit(ch)) {//�޷�����
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
		else { //��������ֽ��
			int pos = 0;
			instring[pos++] = ch;
			instring[pos] = '\0';
			char temp_s[2];
			if ((pointer = a_operator(instring)) != 0) { //���������
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
			else if ((pointer = r_operator(instring)) != 0) {//��ϵ�����
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
			else if ((pointer = delimiterWord(instring)) != 0) {//�ֽ��
				type = 2;
				//cout << instring << endl;
			}
			else errorProcess(type,pointer);
		}
		Print(type, pointer);
	}
}