/*
*******************************************************************************
**               C-Xool toy model to test with ROMS                          **
This script shows how to run C-Xool from the command line using real options,
with a specified grid, time interval, and list of ERA5 variables.
 Authors:
     Carlos Argáez, Simon Klüpfel, María Eugenia Allenda Aranda, Christian Mario Appendini
     To report bugs, questions, feedback or just greetings, please use:
         cargaezg@iingen.unam.mx
*******************************************************************************
**
*/

#define GULFOFMEXICO

#define SOLVE3D
#define MASKING

#define UV_ADV
#define UV_COR
#define UV_VIS2
#define MIX_S_UV

#define DJ_GRADPS
#define TS_U3HADVECTION
#define TS_C4VADVECTION

#define ANA_INITIAL
#define ANA_MASK

#define BULK_FLUXES
#define LONGWAVE
#define SHORTWAVE

#define ANA_BTFLUX
#define ANA_BSFLUX

#define ANA_VISC
#define ANA_DIFF

#define UV_QDRAG


