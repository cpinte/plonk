# cython: language_level=3
# cython: boundscheck=False

cdef extern:

    void interpolate3d_projection_c(
        float *x,
        float *y,
        float *z,
        float *hh,
        float *weight,
        float *dat,
        int   *itype,
        int   *npart,
        float *xmin,
        float *ymin,
        float *datsmooth,
        int   *npixx,
        int   *npixy,
        float *pixwidthx,
        float *pixwidthy,
        bint  *normalise,
        float *zobserver,
        float *dscreen,
        bint  *useaccelerate
        )

    void interpolate3d_proj_vec_c(
        float *x,
        float *y,
        float *z,
        float *hh,
        float *weight,
        float *vecx,
        float *vecy,
        int   *itype,
        int   *npart,
        float *xmin,
        float *ymin,
        float *vectsmoothx,
        float *vectsmoothy,
        int   *npixx,
        int   *npixy,
        float *pixwidthx,
        float *pixwidthy,
        bint  *normalise,
        float *zobserver,
        float *dscreen
        )

    void interpolate3d_fastxsec_c(
        float *x,
        float *y,
        float *z,
        float *hh,
        float *weight,
        float *dat,
        int   *itype,
        int   *npart,
        float *xmin,
        float *ymin,
        float *zslice,
        float *datsmooth,
        int   *npixx,
        int   *npixy,
        float *pixwidthx,
        float *pixwidthy,
        bint  *normalise
        )

    void interpolate3d_xsec_vec_c(
        float *x,
        float *y,
        float *z,
        float *hh,
        float *weight,
        float *vecx,
        float *vecy,
        int   *itype,
        int   *npart,
        float *xmin,
        float *ymin,
        float *zslice,
        float *vectsmoothx,
        float *vectsmoothy,
        int   *npixx,
        int   *npixy,
        float *pixwidthx,
        float *pixwidthy,
        bint  *normalise
        )

    void interp3d_proj_opacity_c(
        float *x,
        float *y,
        float *z,
        float *pmass,
        int   *npmass,
        float *hh,
        float *weight,
        float *dat,
        float *zorig,
        int   *itype,
        int   *npart,
        float *xmin,
        float *ymin,
        float *datsmooth,
        float *brightness,
        int   *npixx,
        int   *npixy,
        float *pixwidth,
        float *zobserver,
        float *dscreenfromobserver,
        float *rkappa,
        float *zcut
        )
