pipeline {
    agent any

    parameters {
        string(name: 'system_name', defaultValue: '直播', description: '系统名称')
        string(name: 'project_name', defaultValue: '微鲸灵', description: '项目名称')
    }

    triggers {
        cron('H 02 * * *')
    }

    environment {
        PATH = "/usr/local/bin:$PATH"
        PYTHON_PATH = 'python3.11'
        SCRIPT_PATH = 'run/scheduler.py'   // 注意，不要加 /，路径拼接容易错
        WORKSPACE_PATH = '/var/jenkins_home/workspace/auto_interface'
        JMETER_PATH = './apache-jmeter-5.6.3/bin/jmeter'
    }

    stages {
        stage('检查Java版本') {
            steps {
                script {
                    def javaVersion = sh(script: 'java -version 2>&1', returnStdout: true).trim()
                    echo "当前Java版本信息:\n${javaVersion}"

                    // 检查是否包含预期的Java版本
                    if (!javaVersion.contains('17')) {
                        error("不支持的Java版本，需要JDK 17")
                    }
                }
            }
        }

        stage('安装依赖') {
            steps {
                sh '''
                    echo "正在安装Python依赖..."
                    ${PYTHON_PATH} -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
                    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
                '''
            }
        }

        stage('准备环境') {
            steps {
                sh '''
                    echo "准备环境中..."

                    # 给 JMeter 授权
                    chmod +x ${JMETER_PATH}

                    # 安装ping工具，注意容器默认无 sudo 权限，这里如果失败就忽略
                    if command -v apt-get >/dev/null; then
                      apt-get update || true
                      apt-get install -y iputils-ping || true
                    fi

                    . venv/bin/activate
                    echo "环境准备好"
                '''
            }
        }

        stage('执行Python脚本') {
            steps {
                script {
                    def fullScriptPath = "${WORKSPACE_PATH}/${SCRIPT_PATH}"
                    sh """
                        . venv/bin/activate
                        ${PYTHON_PATH} ${fullScriptPath} \
                        "${params.system_name}" \
                        "${params.project_name}"
                    """
                }
            }
        }

        stage('生成报告') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'report',
                    reportFiles: 'index.html',
                    reportName: 'Html Report'
                ])
            }
        }
    }

    post {
        always {
            echo '构建过程已完成'
        }
        success {
            echo '自动化脚本执行成功!'
        }
        failure {
            echo '自动化脚本执行失败!'
        }
    }
}