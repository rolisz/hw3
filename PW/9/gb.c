#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define DATAFILE "guestbook.txt"

char* name;
char* message;

void replace_plus(char* src, char* last) {
	for(; src != last; src++) {
		if(*src == '+') {
			*src = ' ';
		}
	}
}
void unencode(char *src, char *last, char *dest)
{
	for(; src != last; src++, dest++) {
		if(*src == '%') {
			int code;
			if(sscanf(src+1, "%2x", &code) != 1) code = '?';
			*dest = code;
			src +=2; 
		}     
		else {
			*dest = *src;
		}
	}
	*dest = '\0';
}

void parse_post(char* query) {
	char* token = strtok (query,"&");
	char *key;
	char *value;
	key = malloc(50);
	value = malloc(250);

	while (token != NULL) {
		sscanf(token, "%[^=]=%s", key, value);
		if (strcmp(key, "name") == 0) {
			unencode(value, value+strlen(value), name);
		}
		if (strcmp(key, "message") == 0) {
			unencode(value, value+strlen(value), message);
			char* le = strstr(message, "<");
			char* ge = strstr(message, ">");
			if (le && ge && le < ge) {
				strcpy(message, "");
			}
		}
		token = strtok(NULL, "&");
	}
}

void show_posts() {
	FILE *f = fopen(DATAFILE,"r");
	char* read;
	char* file_line = malloc(350);
	int day, month, year, hour, minute, second;
	char* name = malloc(50);
	char* message = malloc(250);
	printf("<ul>");
	while ((read = fgets(file_line, 350, f)) != NULL) {
		sscanf(file_line, "%d/%d/%d %d:%d:%d %s %s", &day, &month, &year, &hour, &minute, &second, name, message);
		replace_plus(name,name+strlen(name));
		replace_plus(message, message+strlen(message));
		printf("<li>Message posted by %s at %d/%d/%d %d:%d:%d : %s</li>",name, day, month, year, hour, minute, second, message);
    }
	printf("</ul>");
    fclose(f); 
}

int main(void)
{
	setbuf(stdout, NULL);

	printf("Content-type:text/html\n\n");
	
	printf("<html><head><title>Guest Book</title></head><body>");
	if (stricmp(getenv("REQUEST_METHOD"), "POST") == 0) {
		char* lenstr = getenv("CONTENT_LENGTH");
		int len;
		if(lenstr != NULL) {
			sscanf(lenstr,"%ld",&len);
		}
		if (len > 0) {
			name = malloc(50);
			message = malloc(50);
			
			time_t rawtime;
			struct tm * timeinfo;

			time (&rawtime);
			timeinfo = localtime (&rawtime);
			char* current_time = malloc(100);
			strftime(current_time, 100,"%x %X",timeinfo);
			char input[300];
			fgets(input, len+1, stdin);
			parse_post(input);
			if (strcmp(message, "") == 0) {
				printf("Invalid message!");
				return 0;
			}
			FILE* f = fopen(DATAFILE, "a");
			if(f == NULL) {
				printf("<p>Sorry, cannot store your data.</p>");
				return 0;
			} 
			else {
				fputs(current_time, f);
				fputs(" ", f);
				fputs(name, f);
				fputs(" ", f);
				fputs(message,f);
				fputs("\n", f);
			}
			fclose(f);
			printf("Data written");
		}
	} else {
		show_posts();
		printf("Add a message");
		printf("<form action=gb.cgi method=post>");
		printf("<span>Name</span>");
		printf("<input type=text name=name>");
		printf("<br/>");
		printf("<span>Message</span>");
		printf("<textarea name=message></textarea>");
		printf("<input type=submit value=Send >");
		printf("</form>");
	}
	return 0;
}