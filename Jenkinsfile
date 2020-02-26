properties([
  parameters([
    choice(name: 'DEPLOY_ENV', choices: ['1', '2', '3', '4'], description: 'The target environment', ),
    choice(name: 'PS_VERSION', choices: ['1.7.6.0', '1.7.6.1', '1.7.6.2', '1.7.6.3'], description: 'The prestashop version', )
   ])
])
pipeline {
   agent any

   stages {
      stage('PreLoad') {
         steps {
            echo 'Starting..'
            
            script {
                if ( DEPLOY_ENV < '1' || DEPLOY_ENV > '4') {
                    DEPLOY_ENV = '4'
                }
            }
            
            sh "mkdir -p $DEPLOY_ENV"
            sh "cd $DEPLOY_ENV && docker-compose down"
            //sh "docker-compose down"
         }
      }
      stage('PreBuild') {
         steps {
            sh "wget -N https://github.com/PrestaShop/PrestaShop/archive/${PS_VERSION}.zip"
            sh "unzip ${PS_VERSION}.zip"
            sh "cd PrestaShop-${PS_VERSION} && composer install"
            sh "cd PrestaShop-${PS_VERSION} && export SYMFONY_DEPRECATIONS_HELPER=weak && php -d date.timezone=UTC ./vendor/bin/phpunit -c tests/Unit/phpunit.xml"
            sh "rm -rf PrestaShop-${PS_VERSION} && rm -f ${PS_VERSION}.zip"
         }
      }
      stage('Build') {
         steps {
            sh "wget -N https://raw.githubusercontent.com/thoomson/PS_Docker/master/my-mysql/Dockerfile"
            sh "docker build -t my-mysql ."
            sh "wget -N https://raw.githubusercontent.com/thoomson/PS_Docker/master/my-presta/Dockerfile"
            sh "docker build --build-arg VERSION=${PS_VERSION} -t my-presta ."
            sh "wget -O compose.file -N https://raw.githubusercontent.com/thoomson/PS_Docker/master/docker-compose.yml"
            sh "sed 's/ENVIR/$DEPLOY_ENV/g' compose.file > $DEPLOY_ENV/docker-compose.yml"
         }
      }
      stage('Run') {
         steps {
            sh "cd $DEPLOY_ENV && docker-compose up -d"
         }
      }
      stage('Tests') {
         steps {
            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE')
            {
               sh "wget -N https://raw.githubusercontent.com/thoomson/PS_Docker/master/tests.py"
               sh "export DEPLOY_ENV=$DEPLOY_ENV && python3 tests.py"
            }
         }
      }
      stage('PublishReport') {
         steps {
            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: true, reportDir: 'reports', reportFiles: 'MyReport-ENV-1.html,MyReport-ENV-2.html,MyReport-ENV-3.html,MyReport-ENV-4.html', reportName: 'Tests Dashboard', reportTitles: ''])
         }
      }
   }
}
