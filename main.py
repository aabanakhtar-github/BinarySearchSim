from cmu_graphics import *

# Wrapper around rect to make things easy
class Button:
  def __init__(self, label, x, y, w, h, fill, border):
    self.rect = Rect(x, y, w, h, fill=fill, border=border)
    self.label = Label(label, x + w // 2, y + h // 2, size=10)

  def is_pressed(self, mouseX, mouseY):
    if (self.rect.contains(mouseX, mouseY)):
      return True
    return False

Label("Binary Search Simulator", 300, 10, size=15)
# Configure
app.found_ans_label = Label("No answer found yet", 300, 25)
app.target_label = Label("Target: undetermined", 300, 40)
app.stepsPerSecond = 60
app.mouse_pressed = False
app.next_button = Button("Simulate", 0, 0, 50, 50, "white", 'black')
app.left_label = Label("mid: n/a", 80, 15, size=6)
app.right_label = Label("left: n/a", 80, 25, size=6)
app.mid_label = Label("right: n/a", 80, 35, size=6)
app.ans = Label("best answer: n/a", 80, 45, size=6)
app.sim_step = 0
app.target = -1

def get_app_input_as_int(prompt):
  while True:
    try:
      variable = int(app.getTextInput(prompt))
    except ValueError:
      continue
    else:
      break
  return variable

def simulate_binary_search(arr, target, step):
  curr = 0
  ans = -1
  left = 0
  right = len(arr) - 1

  while left <= right and curr < step:
    mid = left + (right - left) // 2
    curr += 1
    if arr[mid] >= app.target:
      ans = mid
      if curr < step - 1:
        right = mid - 1
    elif curr < step - 1:
      left = mid + 1

  return (ans, left, right, mid)

# Update visualization
def update_bars(bars, left, right, mid, ans):
  for i in bars:
    i[0].fill = "black"

  if left <= right:
    bars[left][0].fill = "green"

  bars[right][0].fill = "red"
  bars[mid][0].fill = "yellow"
  bars[ans][0].fill = "blue"


def onMousePress(x, y):
  if app.next_button.is_pressed(x, y):
    app.sim_step += 1

    ans, left, right, mid = simulate_binary_search(arr, app.target,
                                                   app.sim_step)
    app.left_label.value = "left: " + str(left)
    app.right_label.value = "right: " + str(right)
    app.mid_label.value = "mid: " + str(mid)
    app.ans.value = "best answer: " + str(ans)

    update_bars(bars, left, right, mid, ans)
    
    if left <= right:
      app.left_label.centerX = bars[left][0].centerX
      app.left_label.top = bars[left][0].top - 15

    app.right_label.centerX = bars[right][0].centerX
    app.right_label.top = bars[right][0].top - 30

    app.mid_label.centerX = bars[mid][0].centerX
    app.mid_label.top = bars[mid][0].top - 45

    if app.target == arr[ans]:
      app.ans.centerX = bars[ans][0].centerX
      app.ans.top = bars[ans][0].top - 60
      app.found_ans_label.value = "Found answer at: #" + str(ans)
    elif ans != -1:
      app.ans.centerX = bars[ans][0].centerX
      app.ans.top = bars[ans][0].top - 60
      app.found_ans_label.value = "Found closest answer at: #" + str(ans)
    else:
      app.found_ans_label.value = "No answer yet"

# Run the simulation
arr = []
length = get_app_input_as_int("Enter array length")
for i in range(length):
  elem = get_app_input_as_int('Enter element index #' + str(i))
  arr.append(elem)

# Redundant sort just in case
arr.sort()

# Make bars
app.target = int(app.getTextInput("Input target element"))
app.target_label.value = "Target: " + str(app.target)
bars = []
bar_width = 400 // len(arr)
bar_height = 200 // arr[-1]

j = 0
for i in range(1, bar_width * len(arr) + 1, bar_width):
  bars.append([
      Rect(i, 400 - arr[j] * bar_height, bar_width, arr[j] * bar_height + 1),
      Label(arr[j],
            i + bar_width // 2,
            400 - arr[j] * bar_height + 10,
            fill='white',
            bold=True)
  ])
  j += 1

# Driver code
if __name__ == "__main__":
  cmu_graphics.run()
