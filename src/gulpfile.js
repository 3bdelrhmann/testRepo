var gulp        = require('gulp');
var browserSync = require('browser-sync');
var reload      = browserSync.reload;

gulp.task('default', function() {
    browserSync.init({
        notify: false,
        proxy: "localhost:8000/"
    });
    gulp.watch(['./**/*.{html,py,js,css}'],reload).on('change', browserSync.reload);
});
