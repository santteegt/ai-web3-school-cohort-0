# Interactive learning artifact

I created a skill that builds an interactive quiz around a randomly picked topic from my wiki-like knowledge base. This skill is then executed according to a schedule (e.g. cron job or Claude co-work scheduled task).

## Prompt + Implementation details

See [INTERACTIVE_LEARNING_ARTIFACT.md](/prompts/INTERACTIVE_LEARNING_ARTIFACT.md)

## Skill

See [Quiz Skill](/skills/quiz/SKILL.md)

## Example quiz as scheduled task on Claude CoWork

- Every two hours, the agents picks a random topic and starts an interactive quiz

![quiz1](assets/quiz1.png)

- Each question and answers are rendered as HTMLS UI components using `mcp__visualize__show_widget`

![quiz2](assets/quiz2.png)

- Correct answer's response

![quiz3](assets/quiz3.png)

- Wrong answer's response with a short explanation to refresh the user's knowledge

![quiz4](assets/quiz4.png)

- Quiz session ends with final score and a final review on the topic

![quiz5](assets/quiz5.png)


