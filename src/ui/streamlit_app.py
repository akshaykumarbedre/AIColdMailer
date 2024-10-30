import os
import streamlit as st
import pandas as pd
from ..models.schemas import Target, EmailContent
from ..llm.options import AVAILABLE_MODELS
from ..services.automation import ColdEmailAutomation

class StreamlitUI:
    def __init__(self, automation: ColdEmailAutomation):
        self.automation = automation

    def run(self):
        st.title("Comprehensive Cold Email Automation")

        # Sidebar for configuration
        st.sidebar.header("Model Selection")
        model_key = st.sidebar.selectbox(
            "Choose Language Model",
            options=list(AVAILABLE_MODELS.keys()),
            format_func=lambda x: f"{AVAILABLE_MODELS[x].name} - {AVAILABLE_MODELS[x].description}"
        )
        selected_model = AVAILABLE_MODELS[model_key]

        st.sidebar.header("Email Configuration")
        purpose = st.sidebar.text_input("Purpose of the cold email", 
                               "To offer automated personalized cold email services")
        
        default_prompt = """
        Generate a cold email with the following components:
        1. A compelling subject line that grabs attention
        2. A friendly greeting with talking abut there problem 
        3. An introduction as "Akshay Kumar BM "freelancer who specializes in the specified purpose
        4. A clear value proposition based on the recipient's website content
        5. An offer of a free trial or initial consultation
        6. A call to action (CTA) to engage the recipient
        7. A polite sign-off
        contact information : akshaykumarbedre.bm@gmail.com
        """
        
        custom_prompt = st.sidebar.text_area("Customize the email generation prompt", 
                                    default_prompt, height=200)

        # Main area for target input and email generation
        st.header("Target Input")
        input_method = st.radio("Choose input method:", ["Manual Entry", "Upload CSV"])
        
        targets = []
        if input_method == "Manual Entry":
            num_targets = st.number_input("Number of targets", min_value=1, value=1)
            for i in range(num_targets):
                col1, col2 = st.columns(2)
                with col1:
                    website = st.text_input(f"Website #{i+1}", 
                                          help="Enter a valid URL (e.g., https://example.com)")
                with col2:
                    email = st.text_input(f"Email #{i+1}")
                if website and email:
                    # Basic URL validation
                    if not (website.startswith('http://') or website.startswith('https://')):
                        website = 'https://' + website
                    targets.append(Target(website=website, email=email))
        else:
            uploaded_file = st.file_uploader("Upload CSV with columns 'website' and 'email'", 
                                            type="csv")
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                if 'website' in df.columns and 'email' in df.columns:
                    for _, row in df.iterrows():
                        website = row['website']
                        if not (website.startswith('http://') or website.startswith('https://')):
                            website = 'https://' + website
                        targets.append(Target(website=website, email=row['email']))
                else:
                    st.error("CSV must contain 'website' and 'email' columns")

        if st.button("Generate Emails"):
            if targets:
                progress_bar = st.progress(0)
                success_count = 0
                error_messages = []

                for index, target in enumerate(targets):
                    try:
                        email_content = self.automation.process_target(
                            target, purpose, custom_prompt, selected_model
                        )
                        if email_content:
                            self.automation.save_to_csv(email_content)
                            success_count += 1
                        else:
                            error_messages.append(f"Failed to generate email for {target.website}")
                    except Exception as e:
                        error_messages.append(f"Error processing {target.website}: {str(e)}")
                    finally:
                        progress_bar.progress((index + 1) / len(targets))

                # Show summary of results
                if success_count > 0:
                    st.success(f"Successfully generated {success_count} out of {len(targets)} emails.")
                
                if error_messages:
                    st.error("Encountered the following errors:")
                    for msg in error_messages:
                        st.warning(msg)
            else:
                st.error("Please provide at least one target (website and email).")

        # Email approval and sending section
        st.header("Email Approval and Sending")
        if os.path.exists(self.automation.csv_file):
            df = self.load_csv()
            for _, row in df.iterrows():
                if row['status'] == 'Pending':
                    with st.expander(f"Email for {row['email']} ({row['website']})"):
                        subject = st.text_input(
                            "Subject", 
                            value=row['subject'], 
                            key=f"subject_{row['email']}"
                        )
                        body = st.text_area(
                            "Body", 
                            value=row['body'], 
                            height=300, 
                            key=f"body_{row['email']}"
                        )
                        
                        # Create two columns for Approve and Reject buttons
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("Approve and Send", 
                                       key=f"approve_{row['email']}", 
                                       type="primary"):
                                email_content = EmailContent(
                                    website=row['website'],
                                    email=row['email'],
                                    subject=subject,
                                    body=body
                                )
                                if self.automation.send_email(email_content):
                                    st.success(f"Email sent to {row['email']}")
                                    # Update status in CSV
                                    self.update_email_status(row['email'], 'Sent')
                                else:
                                    st.error(f"Failed to send email to {row['email']}")
                        
                        with col2:
                            if st.button("Reject", 
                                       key=f"reject_{row['email']}", 
                                       type="secondary"):
                                # Update status in CSV to Rejected
                                self.update_email_status(row['email'], 'Rejected')
                                st.info(f"Email to {row['email']} has been rejected")
        
        st.header("Email History")
        if os.path.exists(self.automation.csv_file):
            df = self.load_csv()
            # Add color coding for different statuses
            def color_status(val):
                colors = {
                    'Pending': 'background-color: yellow',
                    'Sent': 'background-color: lightgreen',
                    'Rejected': 'background-color: lightpink'
                }
                return colors.get(val, '')
            
            # Apply color coding to the status column
            styled_df = df.style.applymap(color_status, subset=['status'])
            st.dataframe(styled_df)
        else:
            st.info("No emails have been generated yet.")

    def load_csv(self):
        return pd.read_csv(self.automation.csv_file)

    def update_email_status(self, email, new_status):
        """Update the status of an email in the CSV file."""
        df = self.load_csv()
        df.loc[df['email'] == email, 'status'] = new_status
        df.to_csv(self.automation.csv_file, index=False)