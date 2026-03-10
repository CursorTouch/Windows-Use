# Security Policy

## ⚠️ Critical Security Notice

**Windows-Use directly interacts with your operating system at the GUI layer and executes commands with the same privileges as the user running the agent. There is currently NO sandbox or isolation layer provided.**

### Direct OS Interaction Risks

This project is designed to:
- Control mouse and keyboard inputs
- Launch and interact with applications
- Execute shell commands
- Read and modify files
- Change system settings
- Perform any action a human user could perform through the GUI

**These capabilities mean the agent can:**
- ❌ Delete files or folders
- ❌ Modify system configurations
- ❌ Install or uninstall software
- ❌ Access sensitive data
- ❌ Execute potentially harmful commands
- ❌ Make irreversible changes to your system

## 🛡️ Recommended Deployment Practices

### For Development and Testing

**STRONGLY RECOMMENDED:**
1. **Use a Virtual Machine (VM)**
   - Deploy Windows-Use inside a VM (VirtualBox, VMware, Hyper-V, etc.)
   - Take snapshots before running the agent
   - Isolate the VM from your network if testing untrusted prompts

2. **Use Windows Sandbox**
   - Windows 10/11 Pro/Enterprise includes Windows Sandbox
   - Provides a lightweight, disposable desktop environment
   - Changes are discarded when you close the sandbox

3. **Use a Dedicated Test Machine**
   - Set up a separate physical or virtual machine for testing
   - Do not use your primary work or personal computer

### For Production Deployment

**CRITICAL REQUIREMENTS:**

1. **Isolation is Mandatory**
   - Never deploy on production systems without proper isolation
   - Use containerization or virtualization technologies
   - Implement network segmentation

2. **Access Control**
   - Run the agent with minimal required privileges
   - Create a dedicated user account with restricted permissions
   - Use Windows User Account Control (UAC) appropriately

3. **Monitoring and Auditing**
   - Log all agent actions
   - Monitor system changes in real-time
   - Implement alerting for suspicious activities
   - Review logs regularly

4. **Input Validation**
   - Sanitize and validate all user inputs
   - Implement prompt filtering for dangerous commands
   - Use allowlists for permitted actions when possible

5. **Rate Limiting**
   - Limit the number of actions per time period
   - Implement cooldown periods for destructive operations
   - Add confirmation steps for high-risk actions

## 🔒 Security Best Practices

### Before Running the Agent

- [ ] Review the prompt/query you're providing
- [ ] Understand what actions the agent might take
- [ ] Backup important data
- [ ] Close sensitive applications
- [ ] Ensure you're in a safe environment (VM/Sandbox)

### While Running the Agent

- [ ] Monitor the agent's actions in real-time
- [ ] Be ready to terminate the process if needed
- [ ] Don't leave the agent running unattended
- [ ] Avoid providing prompts that could lead to destructive actions

### After Running the Agent

- [ ] Review what changes were made
- [ ] Check for unexpected file modifications
- [ ] Verify system settings remain as expected
- [ ] Review any logs or telemetry data

## 🚨 Known Security Limitations

### Current Limitations

1. **No Sandboxing**: The agent runs with full user privileges
2. **No Action Filtering**: The agent can attempt any action the LLM decides
3. **No Rollback Mechanism**: Changes made by the agent may be irreversible
4. **LLM Unpredictability**: AI models can misinterpret prompts or make mistakes
5. **No Built-in Safety Rails**: Limited safeguards against destructive operations

### Planned Security Enhancements

We are considering the following security improvements for future releases:
- Action allowlisting/blocklisting
- Confirmation prompts for high-risk operations
- Dry-run mode to preview actions
- Rollback capabilities for certain operations
- Enhanced logging and audit trails
- Integration with security monitoring tools

## 📋 Reporting Security Vulnerabilities

If you discover a security vulnerability in Windows-Use, please report it responsibly:

### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please:
1. Email the maintainer directly at: [jeogeoalukka@gmail.com](mailto:jeogeoalukka@gmail.com)
2. Include detailed information about the vulnerability
3. Provide steps to reproduce if possible
4. Allow reasonable time for a fix before public disclosure

### What to Include

- Description of the vulnerability
- Potential impact
- Steps to reproduce
- Suggested fix (if any)
- Your contact information

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Fix Timeline**: Depends on severity (critical issues prioritized)
- **Public Disclosure**: After fix is released and users have time to update

## 🔐 Security Checklist for Contributors

If you're contributing to Windows-Use, please:

- [ ] Never commit credentials or API keys
- [ ] Review code for potential security issues
- [ ] Test changes in an isolated environment
- [ ] Document any security implications of new features
- [ ] Follow secure coding practices
- [ ] Consider the principle of least privilege
- [ ] Add appropriate warnings to documentation

## ⚖️ Disclaimer

**USE AT YOUR OWN RISK**

Windows-Use is provided "as is" without warranty of any kind. The maintainers and contributors are not responsible for:
- Data loss
- System damage
- Security breaches
- Unintended actions taken by the agent
- Any other damages resulting from the use of this software

By using Windows-Use, you acknowledge and accept these risks.

## 📚 Additional Resources

- [CONTRIBUTING Guidelines](CONTRIBUTING)
- [LICENSE](LICENSE)
- [README](README.md)
- [Project Documentation](https://github.com/CursorTouch/Windows-Use)

## 🆘 Support

For security-related questions (not vulnerabilities):
- Open a GitHub Discussion
- Join our [Discord](https://discord.com/invite/Aue9Yj2VzS)
- Follow [@CursorTouch](https://x.com/CursorTouch) on Twitter

---

**Last Updated**: November 26, 2025  
**Version**: 1.0.0
