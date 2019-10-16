'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var rtlcss = require("gulp-rtlcss");
var rename = require("gulp-rename");
var dl = require('directory-list');
var replace = require('gulp-replace');


gulp.task('sass', ['sass-demo', 'sass-theme'], function () {
});

gulp.task('sass:watch', function () {
    gulp.watch('./sass/**/*.scss', ['sass']);
});

gulp.task('sass-demo', function () {
    dl.list('sass/demos', false, function (demos) {
        demos.forEach(function (demo, i) {
            gulp.src('./sass/demos/' + demo + '/*.scss')
                .pipe(sass({errLogToConsole: true}))
                .pipe(gulp.dest('./assets/demos/' + demo + '/css'));
        });
    });
});

gulp.task('sass-theme', function () {
    dl.list('sass/demos', false, function (demos) {
        demos.forEach(function (demo, i) {
            gulp.src('./sass/core/themes/*.scss')
                .pipe(replace('//##', ''))
                .pipe(replace('{{demo}}', demo))
                .pipe(sass({errLogToConsole: true}))
                .pipe(gulp.dest('./assets/demos/' + demo + '/css/themes'));
        });
    });
});


var prettify = require('gulp-prettify');

gulp.task('prettify', function () {
    gulp.src('../../master/release/theme/*.html')
        .pipe(prettify({
            indent_size: 4,
            indent_inner_html: true,
            unformatted: ['pre', 'code']
        }))
        .pipe(gulp.dest('../../master/release/theme/'))
});

gulp.task('prettify-rtl', function () {
    gulp.src('../../master/release/theme_rtl/*.html')
        .pipe(prettify({
            indent_size: 4,
            indent_inner_html: true,
            unformatted: ['pre', 'code']
        }))
        .pipe(gulp.dest('../../master/release/theme_rtl/'))
});

gulp.task('rtlcss', function () {
    gulp.src(['./assets/demos/**/css/**/*.css', '!./assets/demos/**/*-rtl.css'])
        .pipe(rtlcss())
        .pipe(rename({suffix: '-rtl'}))
        .pipe(gulp.dest('./assets/demos/'));
});