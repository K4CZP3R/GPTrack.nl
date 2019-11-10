from flask import render_template, jsonify

def return_message(title, content, r_time, r_url):
    return render_template('dashboard/message.html',
    title=title,
    content=content,
    r_time=str(r_time),
    r_url=r_url)

def return_api(success:bool, data=None, error=None):
    return jsonify(
        {
            "success": str(success),
            "data": str(data),
            "error": str(error)
        }
    )