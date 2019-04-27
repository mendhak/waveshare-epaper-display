#include <stdlib.h>     //exit()
#include <signal.h>     //signal()
#include <time.h>
#include "GUI_Paint.h"
#include "GUI_BMPfile.h"
#include "ImageData.h"
#include "EPD_7in5.h"

void  Handler(int signo)
{
    //System Exit
    printf("\r\nHandler:Goto Sleep mode\r\n");
    EPD_Sleep();
    DEV_ModuleExit();

    exit(0);
}

int main(int argc, char * argv [])
{
    if(argc != 3){
        printf("Pass in the path to the image and refresh bit (1=refresh, 0=nothing).\n\n");
        printf("Example: ./display /path/myimage.bmp 1\n\n");
        return 1;
    }

 
    // First arg - the path to the bitmap to display
    char *filename = argv[1];

    // All this logic is to figure out if the 2nd arg is a number
    int refresh = 0;
    int errno = 0;
    char *p;   
    long conv = strtol(argv[2], &p, 10);
    
    if (errno != 0 || *p != '\0' || conv > 2) {
        refresh = 0;
    } else {
        // No error
        refresh = conv;    
        printf("%d\n", refresh);
    }

    printf("\r\n");

    DEV_ModuleInit();

    // Exception handling:ctrl + c
    signal(SIGINT, Handler);

    if(EPD_Init() != 0) {
        printf("e-Paper init failed\r\n");
    }
    
    if(refresh == 1){
        printf("clear...\r\n");
        EPD_Clear();
        DEV_Delay_ms(500);
    }
    

    //Create a new image cache
    UBYTE *BlackImage;
    UWORD Imagesize = ((EPD_WIDTH % 8 == 0)? (EPD_WIDTH / 8 ): (EPD_WIDTH / 8 + 1)) * EPD_HEIGHT;
    if((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
        printf("Failed to apply for black memory...\r\n");
        exit(0);
    }
    printf("Paint_NewImage\r\n");
    Paint_NewImage(BlackImage, EPD_WIDTH, EPD_HEIGHT, 0, WHITE);
    Paint_SelectImage(BlackImage);
    Paint_Clear(WHITE);


    printf("show bmp\r\n");
    Paint_SelectImage(BlackImage);  
    Paint_Clear(WHITE);
    GUI_ReadBmp(filename, 0, 0);
    EPD_Display(BlackImage);


    printf("Goto Sleep mode...\r\n");
    EPD_Sleep();
    free(BlackImage);
    BlackImage = NULL;

    return 0;
}
