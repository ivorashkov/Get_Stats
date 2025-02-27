# Get_Stats

sudo apt update
sudo apt install python3
python3 --version
sudo apt install python3-pip
pip3 --version
sudo apt install python3-venv

python3 -m venv pythonenv
source pythonenv/bin/activate

pip install flask psutil

To deactivate the virtual environment:
deactivate

pip freeze > requirements.txt
pip install -r requirements.txt

python python_app.py 

verify metrics:
JSON can be accessed through: http://<your-local-IP>:5000/stats
IP address can be found using ifconfig on Linux/macOS.
make sure port 5000 is open in your firewall settings


test push WF:
git checkout master
git add .
git commit -m "Testing push workflow"
#git push origin master
git tag v1.0.0
git push origin v1.0.0


Test the Pull Request Workflow 
git checkout -b test-pr-branch
git push origin test-pr-branch



      - name: Build new Docker image manually
        run: |
          # Use docker commit to create an image from a container (if needed, otherwise you can skip this)
          docker commit python-stats-app-tag python-stats-app-tag:latest

          # Tag the image manually
          docker tag python-stats-app:latest ivaylorashkov/python-stats-app:${{ env.VERSION }}  # Tag with version
          docker tag python-stats-app:latest ivaylorashkov/python-stats-app:latest  # Always update latest

      - name: Push new Docker image
        run: |
          docker push ivaylorashkov/python-stats-app:${{ env.VERSION }}  # Push with version tag
          docker push ivaylorashkov/python-stats-app:latest  # Always push latest tag