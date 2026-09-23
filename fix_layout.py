import sys

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_card = False
indent_str = ''

for line in lines:
    stripped = line.strip()
    
    if stripped.startswith('st.markdown(') and 'section-card' in stripped:
        in_card = True
        indent_str = line[:len(line) - len(line.lstrip())]
        new_lines.append(indent_str + 'with st.container(border=True):\n')
        continue
        
    if in_card and stripped in [
        'st.markdown("</div>", unsafe_allow_html=True)', 
        "st.markdown('</div>', unsafe_allow_html=True)",
        'st.markdown("</div>", unsafe_allow_html=True)',
        "st.markdown(\"</div>\", unsafe_allow_html=True)"
    ]:
        in_card = False
        continue

    if in_card and line.strip() != '':
        new_lines.append('    ' + line)
    elif in_card and line.strip() == '':
        new_lines.append(line)
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Fixed layout blocks in app.py')
