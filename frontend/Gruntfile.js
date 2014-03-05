'use strict'

module.exports = function(grunt){

  require('load-grunt-tasks')(grunt);

  var buildConfig = {
    src: 'src',
    dist: 'dist'
  };

  grunt.initConfig({
    buildConfig: buildConfig,
    stylus: {
      compile: {
        options: {
          paths: [ '<%= buildConfig.src %>/styl' ],
          use: [
            require('nib'),
            require('stylus-brandcolors'),
            require('stylus-mrmrscolors')
          ],
          'include css': true
        },
        files: {
          '<%= buildConfig.dist %>/css/common.css': '<%= buildConfig.src %>/styl/common.styl',
          '<%= buildConfig.dist %>/css/public.css': '<%= buildConfig.src %>/styl/public.styl',
          '<%= buildConfig.dist %>/css/app.css': '<%= buildConfig.src %>/styl/app.styl'
        }
      }
    },
    copy: {
      bower: {
        files: [
          {
            expand: true,
            cwd: 'bower_components',
            src: [
              'underscore/underscore.js',
              'backbone/backbone.js',
              'jquery/dist/jquery.min.js',
              'jquery/dist/jquery.min.map',
              'requirejs/require.js',
              'requirejs-domready/domReady.js'
            ],
            dest: '<%= buildConfig.dist %>/js/lib',
            flatten: true
          },
          {
            expand: true,
            cwd: 'bower_components/fontawesome',
            src: [
              'css/font-awesome.min.css',
              'fonts/**/*'
            ],
            dest: '<%= buildConfig.dist %>'
          }
        ]
      },
      code: {
        expand: true,
        cwd: '<%= buildConfig.src %>/js',
        src: '**/*.js',
        dest: '<%= buildConfig.dist %>/js'
      }
    },
    clean: {
      dist: [
        '<%= buildConfig.dist %>/css',
        '<%= buildConfig.dist %>/js',
        '<%= buildConfig.dist %>/fonts',
      ]
    },
    watch: {
      styl: {
        files: '<%= buildConfig.src %>/css/styl/**/*',
        tasks: [ 'stylus' ]
      },
      bower: {
        files: '<%= buildConfig.src %>/js/bower_components',
        tasks: [ 'copy:bower' ]
      }
    }
  });

  grunt.registerTask('default', [
    'clean:dist',
    'copy',
    'stylus'
  ]);
};
