#include <iostream>
#include <vector>
#include <string>
class NStatement;
using namespace std;
typedef std::vector<NStatement*> StatementList;

class Node {
public:
    virtual ~Node() {}
    virtual std::string codeGen() { }
};

class NExpression : public Node {
};

class NStatement : public Node {
public:
    std::string codeGen() {
        return "";
    };
};

class NInteger : public NExpression {
public:
    int value;
    NInteger(int value) : value(value) { }
    std::string codeGen() {
        cout<<"mov ax, "<<value<<endl;
        return "";
    };
};


class NVar : public NExpression {
public:
    std::string name;
    NVar(const std::string& name) : name(name) { }
    string codeGen() {
        cout<<"mov ax, "<<name<<endl;
        return "";
    }
};


class NBinaryOperator : public NExpression {
public:
    int op;
    NExpression& lhs;
    NExpression& rhs;
    NBinaryOperator(NExpression& lhs, int op, NExpression& rhs) :
        lhs(lhs), rhs(rhs), op(op) { }
    string codeGen() {
        lhs.codeGen();
        cout<<"mov bx, ax"<<endl;
        rhs.codeGen();
        switch (op) {
            case 0:
                cout<<"add ax, bx"<<endl;
                break;
            case 1:
                cout<<"sub ax, bx"<<endl;
                break;
            case 2:
                cout<<"mul bx"<<endl;
                break;
            case 3:
                cout<<"mov dx, 0"<<endl;
                cout<<"div bx"<<endl;
                break;

        }
        return "";
    }
};

class NAssignment : public NStatement {
public:
    NVar lhs;
    NExpression& rhs;
    NAssignment(NVar lhs, NExpression& rhs) :
        lhs(lhs), rhs(rhs) { }
    string codeGen() {
        rhs.codeGen();
        cout<<"mov "<<lhs.name<<", ax"<<endl;
        return "";
    }
};

class NInput : public NStatement {
public:
    NVar id;
    NInput(NVar id) : id(id) { }
    string codeGen() {
        cout<<"mov ah,0Ah"<<endl;
        cout<<"mov dx, offset maxNrLength"<<endl;
        cout<<"int 21h"<<endl;
        cout<<"call getNumar"<<endl;
        cout<<"mov "<<id.name<<", ax"<<endl;
        return "";
    }
};
class NOutput : public NStatement {
public:
    NVar id;
    NOutput(NVar id) : id(id) { }
    string codeGen() {
        cout<<"mov bx, "<<id.name<<endl;
        cout<<"call getCarac"<<endl;
        cout<<"mov ah, 09h"<<endl;
        cout<<"mov dx, offset sir_caract"<<endl;
        cout<<"int 21h"<<endl;
        return "";
    }
};

#include <vector>
class NProgram : public Node {
public:
    StatementList statements;
    vector<NVar> var_list;
    NProgram() { }
    string codeGen() {
        cout<<"ASSUME cs: code, ds:data"<<endl;
        cout<<"data SEGMENT"<<endl;
        cout<<"maxNrLength db 10 ; lungimea maxima a numarelor citite"<<endl;
        cout<<"nrLength db ? ; lungimea numarului dat de la tastatura"<<endl;
        cout<<"numar_caract db 10 DUP(?) ; numarul dat de la tastatura sub forma de sir de caractere"<<endl;
        cout<<"numar dw 0 ; numarul dat de la tastatura sub forma de numar"<<endl;
        cout<<"zece dw 10"<<endl;
        cout<<"sir_caract db 10 DUP(?) ; numar sub forma de sir de caractere"<<endl;

        vector<NVar>::const_iterator it_var;
        for (it_var = var_list.begin(); it_var != var_list.end(); it_var++) {
            cout<<(*it_var).name<<" dw ?"<<endl;
        }
        cout<<"data ENDS"<<endl;
        cout<<"code SEGMENT"<<endl;
        cout<<"getNumar proc ;transforma sirul de caractere in numar"<<endl;
        cout<<"; punem in cl lungimea sirului de caractere care reprezinta numarul"<<endl;
        cout<<"mov cl,nrLength"<<endl;
        cout<<"mov ch,0"<<endl;
        cout<<"; punem in si offsetul sirului de caractere si setam direction flag la 0"<<endl;
        cout<<"mov si,offset numar_caract"<<endl;
        cout<<"cld"<<endl;
        cout<<"parcurge:"<<endl;
        cout<<"; citim urmatorul caracter si scadem 48 din el pentru a obtine cifra sub forma de numar,  inmultim numarul cu 10 si apoi adunam cifra noua"<<endl;
        cout<<"lodsb"<<endl;
        cout<<"sub al,48"<<endl;
        cout<<"mov bl,10"<<endl;
        cout<<"mov dl, al"<<endl;
        cout<<"mov ax, numar"<<endl;
        cout<<"mul bl"<<endl;
        cout<<"mov dh,0"<<endl;
        cout<<"add ax,dx"<<endl;
        cout<<"mov numar, ax"<<endl;
        cout<<"loop parcurge"<<endl;
        cout<<"mov ax,numar"<<endl;
        cout<<"mov numar, 0"<<endl;
        cout<<"ret"<<endl;
        cout<<"getNumar endp"<<endl;
        cout<<"getCarac proc; transforma numarul in sir de carac"<<endl;
        cout<<"mov di, offset sir_caract + 10"<<endl;
        cout<<"std"<<endl;
        cout<<"mov al, '$'"<<endl;
        cout<<"stosb"<<endl;
        cout<<"impartire:"<<endl;
        cout<<"mov ax,bx"<<endl;
        cout<<"mov dx,0"<<endl;
        cout<<"div zece"<<endl;
        cout<<"mov bx,ax"<<endl;
        cout<<"add dx,48"<<endl;
        cout<<"mov al,dl"<<endl;
        cout<<"stosb"<<endl;
        cout<<"cmp bx,0"<<endl;
        cout<<"jne impartire"<<endl;
        cout<<"ret"<<endl;
        cout<<"getCarac endp"<<endl;
        cout<<"start:"<<endl;
        cout<<"mov ax, data"<<endl;
        cout<<"mov ds, ax"<<endl;
        cout<<"mov es, ax"<<endl;
        StatementList::const_iterator it;
        for (it = statements.begin(); it != statements.end(); it++) {
            (**it).codeGen();
        }
        cout<<"mov ax,4C00h"<<endl;
        cout<<"int 21h"<<endl;
        cout<<"code ends"<<endl;
        cout<<"end start"<<endl;
        return "";
    }
};