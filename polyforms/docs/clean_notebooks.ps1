foreach($i in Get-ChildItem *.ipynb) {
    jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True --inplace $i.Name
}
