# How to Create a New Branch in Git, Develop a New Feature, Test it, and Integrate the Changes in the Main Branch

Here are the steps to create a new branch, develop a new feature, test it, and integrate the changes in the main branch, using command line commands in Bash:

1. Open a terminal window and navigate to the root directory of your Git repository.

2. Check out the main branch by running the following command:
    ```
    git checkout main
    ```

3. Create a new branch to work on the new feature by running the following command:
    ```
    git branch new-feature
    ```

4. Switch to the new branch by running the following command:
    ```
    git checkout new-feature
    ```

5. Develop the new feature by writing code, making changes, and committing your work as you normally would.

6. Test the new feature to make sure it works correctly.

7. When you're ready to integrate the new feature into the main branch, switch back to the main branch by running the following command:
    ```
    git checkout main
    ```

8. Merge the changes from the new-feature branch into the main branch by running the following command:
    ```
    git merge new-feature
    ```

9. Resolve any conflicts that arise during the merge process, if necessary.

10. Test the main branch with the new feature to make sure everything works correctly.

11. If everything looks good, push the changes to the main branch by running the following command:
    ```
    git push origin main
    ```

And that's it! You've successfully created a new branch, developed a new feature in it, tested it, and integrated the changes into the main branch.

# Merge a feature developed on a new branch called "new_feature" and squash all the commits into one before merging:

1. Checkout the branch that you want to merge the new_feature branch into:
   ```
   git checkout main
   ```

2. Merge the new_feature branch into the current branch with the --squash option. This option will merge all the changes from the new_feature branch into the current branch as a single commit:
   ```
   git merge --squash new_feature
   ```

3. Commit the changes by creating a new commit message for the merge commit:
   ```
   git commit -m "Merge new_feature branch with squashed commits"
   ```

4. Push the changes to the remote branch:
   ```
   git push origin main
   ```

And that's it! You have now merged the new_feature branch into the main branch with all the changes squashed into a single commit.
# How to Create a New Branch in Git, Develop a New Feature, Test it, and Integrate the Changes in the Main Branch

Here are the steps to create a new branch, develop a new feature, test it, and integrate the changes in the main branch, using command line commands in Bash:

1. Open a terminal window and navigate to the root directory of your Git repository.

2. Check out the main branch by running the following command:
...
git checkout main
...

3. Create a new branch to work on the new feature by running the following command:

... 
git branch new-feature
... 

4. Switch to the new branch by running the following command:

...
git checkout new-feature
... 

5. Develop the new feature by writing code, making changes, and committing your work as you normally would.

6. Test the new feature to make sure it works correctly.

7. When you're ready to integrate the new feature into the main branch, switch back to the main branch by running the following command:

...
git checkout main
...

8. Merge the changes from the new-feature branch into the main branch by running the following command:

 ```
 git merge new-feature
 ```
 
9. Resolve any conflicts that arise during the merge process, if necessary.

10. Test the main branch with the new feature to make sure everything works correctly.

11. If everything looks good, push the changes to the main branch by running the following command:

 ```
 git push origin main
 ```

And that's it! You've successfully created a new branch, developed a new feature in it, tested it, and integrated the changes into the main branch.

