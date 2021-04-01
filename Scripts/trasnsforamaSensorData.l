/*
    procesador de lenguaje que adapta los datos de los sensores de PRTG para
    poder ser introducidos en Elasticsearch

    Autor: Daniel Mellado 
    
    Compilación:
        flex trasnformaSensorData.l
        gcc lex.yy.c -lfl
*/


%{
 char idSensor[10];
%}

%s DATA
%s PRTGMETADATA
%s READING

%%

"["                         BEGIN(PRTGMETADATA);
<PRTGMETADATA>"{"           {
                                BEGIN(DATA);
                                printf("{\"senosor_id\":\"%s\",",idSensor);


                            }

<DATA>,                     {
                                BEGIN(READING);
                                printf(",\"reading\":{");

                            }

<READING>%                  ;
<READING>"}"                {
                                BEGIN(PRTGMETADATA);
                                printf("}}");

                            }
<READING>.                  printf("%s",yytext);
<PRTGMETADATA>"]"           BEGIN(INITIAL);

<DATA>.                     printf("%s",yytext);
<PRTGMETADATA>,             printf("\n");
<PRTGMETADATA>.|\n          ;

.|\n                        ;


%%

int main(int argc, char **argv){

        if(argc = 2){
                strcpy(idSensor, argv[2]);
                FILE *file;
                file = fopen(argv[1],"r");
                if(!file){
                        printf("No se puede leer el fichero");
                        exit(1);
                }
                yyin = file;
                yylex();

        }else{
                printf("numero de argumentos invalido");
        }


}