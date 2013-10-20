#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define DATAFILE "problems.txt"
int n=1, score=0;

typedef struct line {
	int n;
	char* expr;
	int result;
} line;

void parse_get(char* query) {
	char* token = strtok (query,"&");
	char * key;
	int value;
	while (token != NULL) {
		sscanf(token, "%[^=]=%d", key, &value);
		if (strcmp(key, "n") == 0) {
			n = value;
		}
		token = strtok(NULL, "&");
	}
}

void parse_cookie(char* cookie) {
	char* token = strtok (cookie,";");
	char * key;
	int value;
	while (token != NULL) {
		sscanf(token, "%[^=]=%d", key, &value);
		if (strcmp(key, "score") == 0) {
			score = value;
		}
		token = strtok(NULL, "&");
	}
}

line get_question(int n) {
	FILE *f = fopen(DATAFILE,"r");
	char* read;
	char* file_line = malloc(100);
	int len = 0;
	int nr;
	char* expr = malloc(50);
	int rez;
	char ch;
	while ((read = fgets(file_line, 100, f)) != NULL) {
		sscanf(file_line, "%d %[^=] = %d", &nr, expr, &rez);
		if (nr == n) {
			line l = {nr, expr, rez};
			fclose(f); 
			return l;
		}
    }
    fclose(f); 
	line l = {-1, "", 0};
	return l;
}

int main(void)
{
	int ch;
	char *data = getenv("QUERY_STRING");
	setbuf(stdout, NULL);
	char *cookie = getenv("HTTP_COOKIE");
	parse_cookie(cookie);

	parse_get(data);
	line l = get_question(n);
	char* lenstr = getenv("CONTENT_LENGTH");
	int len;
	if(lenstr != NULL) {
		sscanf(lenstr,"%ld",&len);
	}
	if (len > 0) {
		char data[100], input[100];
		fgets(input, len+1, stdin);
		int res;
		sscanf(input, "result=%d", &res); // 5 vine de la result=
		line prev = get_question(n-1);
		if (prev.result == res) {
			score +=1;
		}
	}
	printf("Set-Cookie: score=%d\n", score);
	printf("Content-type:text/html\n\n");
	
	printf("<html><head><title>Chestionare</title></head><body>");
	if (l.n == -1) {
		printf("Your score is: %d", score);
	}
	else {
		printf("Question number %d", n);
		printf("<form action=form.cgi?n=%d method=post>", n+1);
		printf("<span>%s = </span>", l.expr);
		printf("<input type=text name=result>");
		printf("<input type=submit value=Send >");
		printf("</form>");
	}
	return 0;
}